from argparse import Namespace

from ._get_top import GetTop


class GetTopArtists(GetTop):
    DESCRIPTION: str = "Get your top artists"

    @property
    def item_type(self) -> str:  # pragma: no cover
        return "artists"

    def __init__(self, args: Namespace) -> None:
        self._args: Namespace = args
        for rank, artist in self._results():
            print(rank, artist["name"])
