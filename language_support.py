"""
Language Support Module
Provides translation and language detection for Indian languages.
Supports: English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati
"""

from typing import Dict, Optional, Tuple
from deep_translator import GoogleTranslator
import langdetect
from functools import lru_cache


class LanguageSupport:
    def __init__(self):
        # Supported languages with their codes and native names
        self.supported_languages = {
            'en': {'name': 'English', 'native': 'English', 'flag': '🇬🇧'},
            'hi': {'name': 'Hindi', 'native': 'हिंदी', 'flag': '🇮🇳'},
            'ta': {'name': 'Tamil', 'native': 'தமிழ்', 'flag': '🇮🇳'},
            'te': {'name': 'Telugu', 'native': 'తెలుగు', 'flag': '🇮🇳'},
            'bn': {'name': 'Bengali', 'native': 'বাংলা', 'flag': '🇮🇳'},
            'mr': {'name': 'Marathi', 'native': 'मराठी', 'flag': '🇮🇳'},
            'gu': {'name': 'Gujarati', 'native': 'ગુજરાતી', 'flag': '🇮🇳'}
        }
        
        # Translation cache to avoid redundant API calls
        self._translation_cache = {}
    
    def get_supported_languages(self) -> Dict:
        """Get list of supported languages with metadata."""
        return self.supported_languages
    
    def detect_language(self, text: str) -> str:
        """
        Detect language from text.
        
        Args:
            text: Text to detect language from
            
        Returns:
            Language code (e.g., 'en', 'hi', 'ta')
        """
        if not text or not text.strip():
            return 'en'
        
        try:
            # Use langdetect for detection
            detected = langdetect.detect(text)
            
            # If detected language is supported, return it
            if detected in self.supported_languages:
                return detected
            
            # Default to English if unsupported language
            return 'en'
        except Exception as e:
            print(f"Language detection error: {e}")
            return 'en'
    
    @lru_cache(maxsize=1000)
    def translate_text(
        self, 
        text: str, 
        source_lang: str = 'auto', 
        target_lang: str = 'en'
    ) -> str:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: 'auto' for auto-detect)
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
        
        # If source and target are the same, no translation needed
        if source_lang == target_lang and source_lang != 'auto':
            return text
        
        # Check cache
        cache_key = f"{text}_{source_lang}_{target_lang}"
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]
        
        try:
            # Perform translation using deep-translator
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated_text = translator.translate(text)
            
            # Cache the result
            self._translation_cache[cache_key] = translated_text
            
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            # Return original text if translation fails
            return text
    
    def translate_to_english(self, text: str, source_lang: str = 'auto') -> str:
        """
        Translate text to English for processing.
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: 'auto')
            
        Returns:
            English translation
        """
        return self.translate_text(text, source_lang, 'en')
    
    def translate_from_english(self, text: str, target_lang: str) -> str:
        """
        Translate English text to target language.
        
        Args:
            text: English text to translate
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        if target_lang == 'en':
            return text
        
        return self.translate_text(text, 'en', target_lang)
    
    def is_supported_language(self, lang_code: str) -> bool:
        """Check if language code is supported."""
        return lang_code in self.supported_languages
    
    def get_language_name(self, lang_code: str) -> str:
        """Get language name from code."""
        if lang_code in self.supported_languages:
            return self.supported_languages[lang_code]['name']
        return 'Unknown'
    
    def get_native_name(self, lang_code: str) -> str:
        """Get native language name from code."""
        if lang_code in self.supported_languages:
            return self.supported_languages[lang_code]['native']
        return 'Unknown'
    
    def translate_dict(
        self, 
        data: Dict, 
        source_lang: str = 'en', 
        target_lang: str = 'en'
    ) -> Dict:
        """
        Translate all string values in a dictionary.
        
        Args:
            data: Dictionary with string values
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Dictionary with translated values
        """
        if source_lang == target_lang:
            return data
        
        translated = {}
        for key, value in data.items():
            if isinstance(value, str):
                translated[key] = self.translate_text(value, source_lang, target_lang)
            elif isinstance(value, list):
                translated[key] = [
                    self.translate_text(item, source_lang, target_lang) 
                    if isinstance(item, str) else item 
                    for item in value
                ]
            elif isinstance(value, dict):
                translated[key] = self.translate_dict(value, source_lang, target_lang)
            else:
                translated[key] = value
        
        return translated
    
    def clear_cache(self):
        """Clear translation cache."""
        self._translation_cache.clear()
        self.translate_text.cache_clear()


# Singleton instance
_language_support_instance = None

def get_language_support() -> LanguageSupport:
    """Get or create language support instance."""
    global _language_support_instance
    if _language_support_instance is None:
        _language_support_instance = LanguageSupport()
    return _language_support_instance
