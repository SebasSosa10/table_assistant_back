from abc import ABC, abstractmethod


class AssistantPort(ABC):
    @abstractmethod
    def complete(self, messages: list[dict]) -> str:
        raise NotImplementedError
