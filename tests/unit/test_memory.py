from typing import override

import pytest

from pystores.memory import MemoryStore
from tests.utils.unit import BaseStoreTest, StoreLifespan, StoreLifespanBuilder


class MemoryStoreLifespan[T](StoreLifespan[T]):
    """Lifespan for MemoryStore."""

    def __init__(self, store: MemoryStore[T]) -> None:
        self._store = store

    @override
    async def enter(self) -> MemoryStore[T]:
        return self._store

    @override
    async def exit(self) -> None:
        return None


class MemoryStoreLifespanBuilder[T](StoreLifespanBuilder[T]):
    """Builder for MemoryStoreLifespan."""

    def __init__(self, default: T) -> None:
        self._default = default

    @override
    async def build(self) -> MemoryStoreLifespan[T]:
        return MemoryStoreLifespan(MemoryStore(self._default))


class TestMemoryStore(BaseStoreTest[int]):
    """Tests for MemoryStore."""

    @pytest.fixture
    @override
    def builder(self) -> MemoryStoreLifespanBuilder[int]:
        return MemoryStoreLifespanBuilder(0)

    @pytest.fixture
    @override
    def value(self) -> int:
        return 1

    @pytest.fixture
    @override
    def other_value(self) -> int:
        return 2
