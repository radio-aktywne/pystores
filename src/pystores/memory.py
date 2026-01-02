from typing import override

from pystores.base import Store


class MemoryStore[T](Store[T]):
    """Store that stores the value in memory."""

    def __init__(self, default: T) -> None:
        self._value = default

    @override
    async def get(self) -> T:
        return self._value

    @override
    async def set(self, value: T) -> None:
        self._value = value
