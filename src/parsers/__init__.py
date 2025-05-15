from argparse import ArgumentParser
from collections.abc import Callable

from .number import number
from .verbose import verbose

SHARED: list[Callable[[], ArgumentParser]] = [verbose]
