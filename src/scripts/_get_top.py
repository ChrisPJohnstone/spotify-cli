from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from collections.abc import Iterator
import logging

from ._base import Command
from src.parsers import number, offset, term
from src.spotify import Spotify
from src.type_definitions import JSONObject


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

    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        pass

    def _results(
        self,
        args: Namespace,
        item_type: str,
    ) -> Iterator[tuple[int, JSONObject]]:
        client: Spotify = Spotify()
        for n in range(
            args.offset,
            args.number + args.offset,
            GetTop.MAX_PER_REQUEST,
        ):
            remaining: int = args.number + args.offset - n
            limit: int = min(remaining, GetTop.MAX_PER_REQUEST)
            logging.debug(f"Requesting {item_type} {n}-{limit}")
            yield from client.get_top(item_type, args.term, limit, n)
