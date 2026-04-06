import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ── Constants ─────────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL       = "llama-3.3-70b-versatile"
VECTOR_DB_PATH  = "faiss_index"

# System instructions injected into every prompt
SYSTEM_INSTRUCTIONS = """
IMPORTANT INSTRUCTIONS:
1. If the user describes symptoms, provide clear, empathetic responses.
2. For serious symptoms (chest pain, difficulty breathing, severe bleeding),
   emphasise the need for immediate medical attention.
3. Always consider the user's medical conditions and medications when giving advice.
4. Be supportive and non-judgmental in your responses.
5. Remember the conversation history and maintain context across messages.

FORMATTING INSTRUCTIONS:
- Use Markdown formatting to structure your response.
- Use **Bold** for key terms or important warnings.
- Use bullet points for lists of recommendations or steps.
- Do NOT output a single large paragraph.
"""


class RAGEngine:
    """
    Retrieval-Augmented Generation engine.

    Loads a FAISS vector store built from health documents and uses a
    Groq-hosted LLM to answer user questions with relevant context.
    """

    def __init__(self, vector_db_path: str = VECTOR_DB_PATH):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")

        # Initialise the language model (Groq)
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=api_key,
            model_name=LLM_MODEL,
        )

        # Initialise the sentence-transformer embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_db_path = vector_db_path
        self.vector_store = None

        self._load_vector_store()

    # ── Private helpers ───────────────────────────────────────────────────────

    def _load_vector_store(self) -> None:
        """Load the FAISS index from disk if it exists."""
        if os.path.exists(self.vector_db_path):
            self.vector_store = FAISS.load_local(
                self.vector_db_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            print("Vector store not found. Please run ingest.py first.")

    def _build_history_context(self, conversation_history: list) -> str:
        """Format the last 5 chat turns into a readable context string."""
        if not conversation_history:
            return ""

        recent = conversation_history[-5:]
        lines = []
        for turn in recent:
            lines.append(f"User: {turn.get('message', '')}")
            lines.append(f"Assistant: {turn.get('response', '')}")

        return "\n\nPrevious conversation:\n" + "\n".join(lines) + "\n"

    def _build_prompt_template(
        self,
        profile_section: str,
        history_context: str,
    ) -> PromptTemplate:
        """Assemble the full prompt template with profile and history injected."""
        template = (
            f"Use the following pieces of context to answer the question at the end."
            f"{profile_section}"
            f"{history_context}"
            "\nIf you don't know the answer, say so — do not make up an answer."
            "\nWhen giving recommendations, ALWAYS consider the user's health profile."
            f"\n{SYSTEM_INSTRUCTIONS}"
            "\nContext: {context}"
            "\n\nQuestion: {question}"
            "\n\nAnswer:"
        )
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"],
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def generate_response(
        self,
        query: str,
        user_profile_context: str = "",
        conversation_history: list = None,
    ) -> str:
        """
        Generate an AI response for the given query.

        Args:
            query:                 The user's question (in English).
            user_profile_context:  Formatted string of the user's health profile.
            conversation_history:  List of previous chat interactions.

        Returns:
            The model's answer as a string.
        """
        if not self.vector_store:
            return "System not initialised. Please ensure data is ingested."

        profile_section = f"\n\n{user_profile_context}\n" if user_profile_context else ""
        history_context = self._build_history_context(conversation_history or [])
        prompt          = self._build_prompt_template(profile_section, history_context)

        # LCEL chain: retrieve docs → format → prompt → LLM → parse string
        retriever = self.vector_store.as_retriever()
        chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke(query)

    @staticmethod
    def _format_docs(docs) -> str:
        """Concatenate retrieved document chunks into a single context string."""
        return "\n\n".join(doc.page_content for doc in docs)
