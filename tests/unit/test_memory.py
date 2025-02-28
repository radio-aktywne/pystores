import pytest

from pystores.memory import MemoryStore
from tests.utils.unit import BaseStoreTest, StoreLifespan, StoreLifespanBuilder


class MemoryStoreLifespan[T](StoreLifespan[T]):
    def __init__(self, store: MemoryStore[T]) -> None:
        self._store = store

    async def enter(self) -> MemoryStore[T]:
        return self._store

    async def exit(self) -> None:
        return None


class MemoryStoreLifespanBuilder[T](StoreLifespanBuilder[T]):
    def __init__(self, default: T) -> None:
        self._default = default

    async def build(self) -> MemoryStoreLifespan[T]:
        return MemoryStoreLifespan(MemoryStore(self._default))


class TestMemoryStore(BaseStoreTest[int]):
    @pytest.fixture
    def builder(self) -> MemoryStoreLifespanBuilder[int]:
        return MemoryStoreLifespanBuilder(0)

    @pytest.fixture
    def value(self) -> int:
        return 1

    @pytest.fixture
    def other_value(self) -> int:
        return 2
