from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from collections.abc import Iterator

from ._base import Command
from src.parsers import number, offset, term
from src.spotify import Spotify
from src.type_definitions import JSONObject


class GetTop(Command):
    DEFAULT_LIMIT: int = 20
    DEFAULT_OFFSET: int = 0
    DEFAULT_TERM: str = "medium_term"

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

    def _results(self, args: Namespace, item_type: str) -> Iterator[JSONObject]:
        client: Spotify = Spotify()
        yield from client.get_top(
            item_type=item_type,
            term=args.term,
            limit=args.number,
            offset=args.offset,
        )
