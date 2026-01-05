from services.base_service import BaseService


class SearchService(BaseService):

    def search(self, query, size=20, page=None, language="en"):
        params = {"q": query, "size": size, "language": language}

        if page is not None:
            params["page"] = page

        return self._get("/content/api/v4/search", params)
