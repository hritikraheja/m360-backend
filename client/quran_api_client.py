from auth.impl.oauth_token_provider import OAuthTokenProvider
from http_client.impl.requests_http_client import RequestsHttpClient
from services.impl.audio_service import AudioService
from services.impl.chapter_service import ChapterService
from services.impl.resource_service import ResourceService
from services.impl.search_service import SearchService
from services.impl.verse_service import VerseService


class QuranApiClient:

    def __init__(self, config):
        token_provider = OAuthTokenProvider(config)
        http_client = RequestsHttpClient()

        self.chapters = ChapterService(config, token_provider, http_client)
        self.verses = VerseService(config, token_provider, http_client)
        self.resources = ResourceService(config, token_provider, http_client)
        self.search = SearchService(config, token_provider, http_client)
        self.audio = AudioService(config, token_provider, http_client)
