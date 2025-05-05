from abc import ABC, abstractmethod


class BaseCloudProvider(ABC):
    @abstractmethod
    def authenticate(self, client_id: str, client_secret: str, email: str):
        pass
