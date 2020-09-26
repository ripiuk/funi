import typing as typ

from funi.providers import banks
from funi.providers._base import AbstractProvider

PROVIDERS: typ.Tuple[typ.Type[AbstractProvider], ...] = (
    banks.Bank1,
    banks.Bank2,
)
