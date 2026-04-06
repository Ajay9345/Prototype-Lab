import os
import json
import base64
from groq import Groq


# ── Allowed image extensions for uploads ──────────────────────────────────────
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def is_allowed_file(filename: str) -> bool:
    """Return True if the file extension is in the allowed set."""
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


def save_temp_image(file, folder: str, prefix: str = "") -> str:
    """
    Save an uploaded file to a temporary path inside `folder`.

    Args:
        file:   Flask FileStorage object.
        folder: Directory to save the file in (created if missing).
        prefix: Optional filename prefix (e.g. 'food_', 'receipt_').

    Returns:
        Full path to the saved file.
    """
    from werkzeug.utils import secure_filename

    os.makedirs(folder, exist_ok=True)
    filename = secure_filename(file.filename)
    temp_path = os.path.join(folder, f"{prefix}{filename}")
    file.save(temp_path)
    return temp_path


def remove_file_if_exists(path: str) -> None:
    """Delete a file silently if it exists."""
    if os.path.exists(path):
        os.remove(path)


def encode_image_to_base64(image_path: str) -> str:
    """Read an image file and return its base64-encoded string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_vision_message(prompt: str, base64_image: str) -> list:
    """
    Build the messages list for a Groq vision (multimodal) API call.

    Args:
        prompt:       Text prompt to send alongside the image.
        base64_image: Base64-encoded image string.

    Returns:
        List with a single user message containing text + image.
    """
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ]


def get_groq_client() -> Groq | None:
    """
    Create and return a Groq client using the GROQ_API_KEY env variable.
    Returns None if the key is missing or the client fails to initialise.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        return Groq(api_key=api_key) if api_key else None
    except Exception:
        return None


def call_groq_json(
    client: Groq,
    model: str,
    messages: list,
    system_prompt: str = "",
    temperature: float = 0.1,
    max_tokens: int = 1000,
) -> dict:
    """
    Call the Groq chat API and parse the JSON response.

    Args:
        client:        Groq client instance.
        model:         Model name to use.
        messages:      List of message dicts.
        system_prompt: Optional system-role message.
        temperature:   Sampling temperature.
        max_tokens:    Maximum tokens in the response.

    Returns:
        Parsed JSON dict from the model response.

    Raises:
        Exception if the API call or JSON parsing fails.
    """
    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    response = client.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)
