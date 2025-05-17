from argparse import Namespace

from ._get_top import GetTop


class GetTopTracks(GetTop):
    DESCRIPTION: str = "Get your top tracks"

    @property
    def item_type(self) -> str:  # pragma: no cover
        return "tracks"

    def __init__(self, args: Namespace) -> None:
        self._args: Namespace = args
        for rank, track in self._results():
            artists: list[str] = [artist["name"] for artist in track["artists"]]
            print(rank, track["name"], "by", ", ".join(artists))
