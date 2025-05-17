from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from collections.abc import Iterator
import logging

from ._base import Command
from parsers import number, offset, term
from spotify import Spotify
from type_definitions import JSONObject


class GetTop(Command):
    DEFAULT_LIMIT: int = 20
    DEFAULT_OFFSET: int = 0
    DEFAULT_TERM: str = "medium_term"
    MAX_PER_REQUEST: int = 50

    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [
            number(GetTop.DEFAULT_LIMIT, "Number of tracks to pull"),
            offset(GetTop.DEFAULT_OFFSET, "Rank to start pulling from"),
            term(
                default=GetTop.DEFAULT_TERM,
                help_string="Over what time frame affinity is computed",
            ),
        ]

    @property
    def args(self) -> Namespace:  # pragma: no cover
        if not hasattr(self, "_args"):
            raise ValueError("_args must be set by init")
        return self._args  # type: ignore

    @property
    @abstractmethod
    def item_type(self) -> str:  # pragma: no cover
        pass

    @abstractmethod
    def __init__(self, args: Namespace) -> None:  # pragma: no cover
        pass

    def _results(self) -> Iterator[tuple[int, JSONObject]]:
        client: Spotify = Spotify()
        for n in range(
            self.args.offset,
            self.args.number + self.args.offset,
            GetTop.MAX_PER_REQUEST,
        ):
            remaining: int = self.args.number + self.args.offset - n
            limit: int = min(remaining, GetTop.MAX_PER_REQUEST)
            logging.debug(f"Requesting {self.item_type} {n}-{limit + n}")
            yield from client.get_top(self.item_type, self.args.term, limit, n)
