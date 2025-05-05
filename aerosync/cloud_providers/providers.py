from enum import Enum


class CloudProviders(Enum):
    GDRIVE = "gdrive"

    @classmethod
    def exists(cls, provider: str) -> bool:
        """Check if the provider exists in the CloudProviders enum."""
        return provider.upper() in cls.__members__
