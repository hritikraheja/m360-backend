from enum import Enum


class OAuth2Urls(Enum):
    TOKEN_ENDPOINT = "/oauth2/token"
    INTROSPECT_ENDPOINT = "/oauth2/introspect"
