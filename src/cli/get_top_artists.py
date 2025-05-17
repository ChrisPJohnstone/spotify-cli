from argparse import Namespace

from ._get_top import GetTop


class GetTopArtists(GetTop):
    @property
    def item_type(self) -> str:
        return "artists"

    def __init__(self, args: Namespace) -> None:
        self._args: Namespace = args
        for rank, artist in self._results():
            print(rank, artist["name"])
