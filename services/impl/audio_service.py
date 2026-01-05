from services.base_service import BaseService


class AudioService(BaseService):

    def get_chapter_recitation_audio(self, chapter_id, recitation_id):
        return self._get(
            f"/content/api/v4/chapter_recitations/{recitation_id}/{chapter_id}"
        )
