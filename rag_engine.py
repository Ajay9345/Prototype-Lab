import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

load_dotenv()

class RAGEngine:
    def __init__(self, vector_db_path="faiss_index"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=self.api_key,
            model_name="llama-3.3-70b-versatile"
        )
        
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_db_path = vector_db_path
        self.vector_store = None
        self.qa_chain = None
        
        self.load_vector_store()

    def load_vector_store(self):
        if os.path.exists(self.vector_db_path):
            self.vector_store = FAISS.load_local(self.vector_db_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            print("Vector store not found. Please run ingest.py first.")

    def setup_qa_chain(self):
        # Note: We'll use a custom prompt that gets updated per query
        # This is a placeholder chain setup
        pass

    def generate_response(self, query, user_profile_context="", conversation_history=None):
        if not self.vector_store:
            return "System not initialized. Please ensure data is ingested."
        
        # Build conversation history context
        history_context = ""
        if conversation_history and len(conversation_history) > 0:
            # Include last 5 interactions for context
            recent_history = conversation_history[-5:]
            history_parts = []
            for interaction in recent_history:
                history_parts.append(f"User: {interaction.get('message', '')}")
                history_parts.append(f"Assistant: {interaction.get('response', '')}")
            history_context = "\n\nPrevious conversation:\n" + "\n".join(history_parts) + "\n"
        
        # Build personalized prompt template
        profile_section = f"\n\n{user_profile_context}\n" if user_profile_context else ""
        
        prompt_template = f"""Use the following pieces of context to answer the question at the end.{profile_section}{history_context}
If you don't know the answer, just say that you don't know, don't try to make up an answer.
When providing recommendations, ALWAYS consider the user's health profile (age, conditions, allergies, medications) if provided.
Tailor your advice specifically to their situation.

IMPORTANT INSTRUCTIONS:
1. If the user describes symptoms, provide clear, empathetic responses
2. For serious symptoms (chest pain, difficulty breathing, severe bleeding), emphasize the need for immediate medical attention
3. Always consider the user's medical conditions and medications when giving advice
4. Provide evidence-based information from the context
5. Be supportive and non-judgmental in your responses
6. If discussing symptoms, ask relevant follow-up questions to better understand the situation
7. Remember the conversation history and maintain context across messages
8. Refer back to previous messages when relevant

FORMATTING INSTRUCTIONS:
- Use Markdown formatting to structure your response.
- Use **Bold** for key terms or important warnings.
- Use bullet points for lists of recommendations or steps.
- Separate different sections (e.g., Analysis, Recommendations, Questions) with newlines.
- Do NOT output a single large paragraph. Break it down into readable chunks.

Context: {{context}}

Question: {{question}}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        response = qa_chain.invoke({"query": query})
        return response['result']

if __name__ == "__main__":
    # Test
    try:
        engine = RAGEngine()
        print(engine.generate_response("How much water should I drink?"))
    except Exception as e:
        print(f"Error: {e}")
