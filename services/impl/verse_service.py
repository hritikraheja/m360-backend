from services.base_service import BaseService


class VerseService(BaseService):

    def by_key(self, verse_key, language="en", translations=None, words=False):
        params = {"language": language}
        if translations:
            params["translations"] = ",".join(map(str, translations))
        if words:
            params["words"] = "true"
        return self._get(f"/content/api/v4/verses/by_key/{verse_key}", params)
