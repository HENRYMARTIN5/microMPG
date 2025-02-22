from abc import ABC, abstractmethod
from typing import List


class Backend(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def read(self) -> List[int|float]:
        pass
