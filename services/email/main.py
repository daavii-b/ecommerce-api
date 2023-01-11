from abc import ABC, abstractmethod
from typing import Any, List


class IEmailService(ABC):

    @abstractmethod
    def __init__(
        self,
        subject: str,
        message: str,
        recipient_list: List[str],
        fail_silently: bool,
        html_message,
        connection: Any,
    ) -> None:
        self.__from_email: str

    @property
    @abstractmethod
    def subject(self) -> str:
        pass

    @property
    @abstractmethod
    def message(self) -> str:
        pass

    @property
    @abstractmethod
    def recipient_list(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def fail_silently(self) -> bool:
        pass

    @property
    @abstractmethod
    def html_message(self) -> str:
        pass

    @property
    @abstractmethod
    def connection(self) -> Any:
        pass

    @subject.setter
    @abstractmethod
    def subject(self, value: str) -> str:
        pass

    @message.setter
    @abstractmethod
    def message(self, value: str) -> str:
        pass

    @recipient_list.setter
    @abstractmethod
    def recipient_list(self, value: List[str]) -> List[str]:
        pass

    @fail_silently.setter
    @abstractmethod
    def fail_silently(self, value: bool) -> bool:
        pass

    @html_message.setter
    @abstractmethod
    def html_message(self, value: str) -> str:
        pass

    @connection.setter
    @abstractmethod
    def connection(self, value: Any) -> Any:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def send_email(self) -> None:
        pass
