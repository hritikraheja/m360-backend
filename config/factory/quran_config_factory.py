import os
from dotenv import load_dotenv
from config.quran_api_config import QuranApiConfig
from constants.environment import Environment


class QuranConfigFactory:

    @staticmethod
    def create():
        env = os.getenv("APP_ENV", Environment.PREPROD.value).lower()

        if env == Environment.PROD.value:
            env_file = ".env.prod"
        elif env == Environment.PREPROD.value:
            env_file = ".env.preprod"
        elif env == Environment.DEV.value:
            env_file = ".env.dev"
        elif env == Environment.LOCAL.value:
            env_file = ".env.local"
        else:
            raise ValueError(
                f"Unsupported environment: {env}. "
                f"Supported: {[e.value for e in Environment]}"
            )

        load_dotenv(env_file, override=True)

        required_vars = [
            "QURAN_CLIENT_ID",
            "QURAN_CLIENT_SECRET",
            "QURAN_BASE_URL",
            "QURAN_OAUTH_URL",
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        return QuranApiConfig(
            client_id=os.getenv("QURAN_CLIENT_ID"),
            client_secret=os.getenv("QURAN_CLIENT_SECRET"),
            base_url=os.getenv("QURAN_BASE_URL"),
            oauth_url=os.getenv("QURAN_OAUTH_URL"),
        )
