from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import pytest

from pystores.base import Store

T = TypeVar("T")


class StoreLifespan(Generic[T], ABC):
    """Base class for managing the lifespan of a store."""

    async def __aenter__(self) -> Store[T]:
        return await self.enter()

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.exit()

    @abstractmethod
    async def enter(self) -> Store[T]:
        """Enter the lifespan of the store."""

        pass

    @abstractmethod
    async def exit(self) -> None:
        """Exit the lifespan of the store."""

        pass


class StoreLifespanBuilder(Generic[T], ABC):
    """Base class for building a store lifespan."""

    @abstractmethod
    async def build(self) -> StoreLifespan[T]:
        """Build a store lifespan."""

        pass


class BaseStoreTest(Generic[T], ABC):
    """Base class for testing a store."""

    @pytest.fixture()
    @abstractmethod
    def builder(self) -> StoreLifespanBuilder[T]:
        """Return a builder for a store lifespan."""

        pass

    @pytest.fixture()
    @abstractmethod
    def value(self) -> T:
        """Return some test value."""

        pass

    @pytest.fixture()
    @abstractmethod
    def other_value(self) -> T:
        """Return some other test value."""

        pass

    @pytest.mark.asyncio(scope="session")
    async def test_get_set(
        self, builder: StoreLifespanBuilder[T], value: T, other_value: T
    ) -> None:
        """Test getting and setting a value."""

        async with (await builder.build()) as store:
            await store.set(value)
            assert await store.get() == value
            await store.set(other_value)
            assert await store.get() == other_value
