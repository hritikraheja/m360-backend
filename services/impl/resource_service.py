from services.base_service import BaseService


class ResourceService(BaseService):

    def translations(self, language=None):
        return self._get(
            "/content/api/v4/resources/translations",
            {"language": language} if language else {},
        )
