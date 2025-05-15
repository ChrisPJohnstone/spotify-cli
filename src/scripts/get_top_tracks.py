from argparse import Namespace

from ._get_top import GetTop


class GetTopTracks(GetTop):
    def __init__(self, args: Namespace) -> None:
        for rank, track in self._results(args, "tracks"):
            artists: list[str] = [artist["name"] for artist in track["artists"]]
            print(rank, track["name"], "by", ",".join(artists))
