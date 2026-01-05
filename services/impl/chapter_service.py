from services.base_service import BaseService


class ChapterService(BaseService):

    def get_chapters(self, language="en"):
        return self._get("/content/api/v4/chapters", {"language": language})

    def get_chapter(self, chapter_id, language="en"):
        return self._get(
            f"/content/api/v4/chapters/{chapter_id}", {"language": language}
        )
