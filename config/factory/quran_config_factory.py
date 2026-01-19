import os
from dotenv import load_dotenv
from config.quran_api_config import QuranApiConfig
from constants.environment import Environment


class QuranConfigFactory:

    @staticmethod
    def _detect_env_file():
        env_files = {
            Environment.PROD.value: ".env.prod",
            Environment.PREPROD.value: ".env.preprod",
            Environment.DEV.value: ".env.dev",
            Environment.LOCAL.value: ".env.local",
        }

        for env_name, env_file in env_files.items():
            if os.path.exists(env_file):
                return env_name, env_file

        if os.path.exists(".env"):
            return None, ".env"
        
        return None, None

    @staticmethod
    def create():
        if os.path.exists(".env"):
            load_dotenv(".env", override=False)
        env = os.getenv("APP_ENV")
        env_file = None
        
        if env:
            env = env.lower()
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
        else:
            detected_env, detected_file = QuranConfigFactory._detect_env_file()
            if detected_file:
                env_file = detected_file
                env = detected_env if detected_env else Environment.PREPROD.value
            else:
                env = Environment.PREPROD.value
                env_file = ".env.preprod"

        if env_file and os.path.exists(env_file):
            load_dotenv(env_file, override=True)
        elif not os.path.exists(".env"):
            import warnings
            warnings.warn(
                f"Environment file {env_file} not found. Using system environment variables."
            )

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
