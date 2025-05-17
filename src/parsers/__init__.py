from collections.abc import Callable

from .device import device
from .number import number
from .offset import offset
from .term import term
from .verbose import verbose

SHARED: list[Callable] = [verbose]
