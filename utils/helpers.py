import os
import json
import base64
from groq import Groq

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024


def is_allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_temp_image(file, folder: str, prefix: str = "") -> str:
    from werkzeug.utils import secure_filename
    os.makedirs(folder, exist_ok=True)
    filename = secure_filename(file.filename)
    temp_path = os.path.join(folder, f"{prefix}{filename}")
    file.save(temp_path)
    return temp_path


def remove_file_if_exists(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_vision_message(prompt: str, base64_image: str) -> list:
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ]


def get_groq_client() -> Groq | None:
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
