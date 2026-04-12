from typing import Dict, Optional
from deep_translator import GoogleTranslator
import langdetect
from functools import lru_cache

SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {"name": "English",  "native": "English",    "flag": "🇬🇧"},
    "hi": {"name": "Hindi",    "native": "हिंदी",       "flag": "🇮🇳"},
    "ta": {"name": "Tamil",    "native": "தமிழ்",       "flag": "🇮🇳"},
    "te": {"name": "Telugu",   "native": "తెలుగు",      "flag": "🇮🇳"},
    "bn": {"name": "Bengali",  "native": "বাংলা",       "flag": "🇮🇳"},
    "mr": {"name": "Marathi",  "native": "मराठी",       "flag": "🇮🇳"},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી",     "flag": "🇮🇳"},
}


class LanguageSupport:
    def __init__(self):
        self._cache: Dict[str, str] = {}

    def get_supported_languages(self) -> Dict:
        return SUPPORTED_LANGUAGES

    def is_supported_language(self, lang_code: str) -> bool:
        return lang_code in SUPPORTED_LANGUAGES

    def get_language_name(self, lang_code: str) -> str:
        return SUPPORTED_LANGUAGES.get(lang_code, {}).get("name", "Unknown")

    def get_native_name(self, lang_code: str) -> str:
        return SUPPORTED_LANGUAGES.get(lang_code, {}).get("native", "Unknown")

    def detect_language(self, text: str) -> str:
        if not text or not text.strip():
            return "en"
        try:
            detected = langdetect.detect(text)
            return detected if detected in SUPPORTED_LANGUAGES else "en"
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en"

    @lru_cache(maxsize=1000)
    def translate_text(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
        if not text or not text.strip():
            return text
        if source_lang == target_lang and source_lang != "auto":
            return text

        cache_key = f"{text}|{source_lang}|{target_lang}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
            self._cache[cache_key] = translated
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def translate_to_english(self, text: str, source_lang: str = "auto") -> str:
        return self.translate_text(text, source_lang, "en")

    def translate_from_english(self, text: str, target_lang: str) -> str:
        if target_lang == "en":
            return text
        return self.translate_text(text, "en", target_lang)

    def translate_dict(self, data: Dict, source_lang: str = "en", target_lang: str = "en") -> Dict:
        if source_lang == target_lang:
            return data

        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.translate_text(value, source_lang, target_lang)
            elif isinstance(value, list):
                result[key] = [
                    self.translate_text(item, source_lang, target_lang) if isinstance(item, str) else item
                    for item in value
                ]
            elif isinstance(value, dict):
                result[key] = self.translate_dict(value, source_lang, target_lang)
            else:
                result[key] = value
        return result

    def clear_cache(self) -> None:
        self._cache.clear()
        self.translate_text.cache_clear()


_instance: Optional[LanguageSupport] = None


def get_language_support() -> LanguageSupport:
    global _instance
    if _instance is None:
        _instance = LanguageSupport()
    return _instance
