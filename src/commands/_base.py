from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace


class Command(ABC):
    @staticmethod
    @abstractmethod
    def parent_parsers() -> list[ArgumentParser]:  # pragma: no cover
        pass

    @abstractmethod
    def __init__(self, args: Namespace) -> None:  # pragma: no cover
        pass
