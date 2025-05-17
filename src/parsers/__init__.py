from argparse import ArgumentParser
from collections.abc import Callable
from typing import Optional

from .number import number
from .offset import offset
from .term import term
from .verbose import verbose

SHARED: list[Callable] = [verbose]
