from argparse import Namespace

from ._get_top import GetTop


class GetTopTracks(GetTop):
    DESCRIPTION: str = "Get your top tracks"

    @property
    def item_type(self) -> str:  # pragma: no cover
        return "tracks"

    def __init__(self, args: Namespace) -> None:
        self._args: Namespace = args
        max_rank_len: int = len(str(args.number + args.offset))
        for rank, track in self._results():
            rank_string: str = f"{rank:0{max_rank_len}d}"
            artists: list[str] = [artist["name"] for artist in track["artists"]]
            print(f"{rank_string} {track['name']:<50}{', '.join(artists)}")
