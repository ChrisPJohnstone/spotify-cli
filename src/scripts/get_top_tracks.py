from argparse import Namespace

from ._get_top import GetTop


class GetTopTracks(GetTop):
    def __init__(self, args: Namespace) -> None:
        for track in self._results(args, "artists"):
            artists: list[str] = [artist["name"] for artist in track["artists"]]
            print("".join(artists), track["name"])
