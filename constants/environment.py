from enum import Enum


class Environment(Enum):
    PROD = "prod"
    PREPROD = "preprod"
    DEV = "dev"
    LOCAL = "local"
