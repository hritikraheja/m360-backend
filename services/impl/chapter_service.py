from services.base_service import BaseService
from utils.auto_translator import translate_text, LANG_CODE_TO_NAME


def localize_chapters(data, language="en"):
    """
    Safely adjust chapter payload to include proper translated_name.language_name
    and act as a no-op for languages that don't need localization.

    This function intentionally avoids mutating translated names because a
    generic translation pass happens elsewhere for non-English/Arabic.
    """
    try:
        if not isinstance(data, dict):
            return data
        lang = (language or "en").strip().lower()

        # Determine readable language name for metadata
        lang_name = LANG_CODE_TO_NAME.get(lang, lang)

        # Handle list payload
        chapters = data.get("chapters")
        if isinstance(chapters, list):
            for ch in chapters:
                if isinstance(ch, dict):
                    t = ch.get("translated_name")
                    if isinstance(t, dict):
                        # Only set language name metadata; do not alter actual name here
                        t["language_name"] = lang_name
            return data

        # Handle single item payload
        ch = data.get("chapter")
        if isinstance(ch, dict):
            t = ch.get("translated_name")
            if isinstance(t, dict):
                t["language_name"] = lang_name
        return data
    except Exception:
        # Be defensive: never break the response shaping
        return data


class ChapterService(BaseService):

    def get_chapters(self, language="en"):
        data = self._get("/content/api/v4/chapters", {"language": language})
        # Apply static Hindi localization if enabled (precise mapping)
        if getattr(self.config, "use_local_chapter_translations", True):
            data = localize_chapters(data, language)
        # Generic translation fallback for translated_name if still not in requested language
        if language and language not in ("en", "ar"):
            chapters = data.get("chapters") if isinstance(data, dict) else None
            if chapters and isinstance(chapters, list):
                for ch in chapters:
                    t = ch.get("translated_name") if isinstance(ch, dict) else None
                    if t and isinstance(t, dict) and t.get("name"):
                        t["name"] = translate_text(t.get("name"), target_language=language)
                        t["language_name"] = {
                            "hi": "hindi",
                            "en": "english",
                            "ar": "arabic",
                        }.get(language, language)
        return data

    def get_chapter(self, chapter_id, language="en"):
        data = self._get(
            f"/content/api/v4/chapters/{chapter_id}", {"language": language}
        )
        if getattr(self.config, "use_local_chapter_translations", True):
            data = localize_chapters(data, language)
        if language and language not in ("en", "ar") and isinstance(data, dict):
            ch = data.get("chapter")
            if ch and isinstance(ch, dict):
                t = ch.get("translated_name")
                if t and isinstance(t, dict) and t.get("name"):
                    t["name"] = translate_text(t.get("name"), target_language=language)
                    t["language_name"] = {
                        "hi": "hindi",
                        "en": "english",
                        "ar": "arabic",
                    }.get(language, language)
        return data
