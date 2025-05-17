from argparse import Namespace

from ._get_top import GetTop


class GetTopArtists(GetTop):
    def __init__(self, args: Namespace) -> None:
        for rank, artist in self._results(args, "artists"):
            print(rank, artist["name"])
