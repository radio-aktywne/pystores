from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Store(Generic[T], ABC):
    """Base class for stores."""

    @abstractmethod
    async def get(self) -> T:
        """Return the stored value."""

        pass

    @abstractmethod
    async def set(self, value: T) -> None:
        """Set the stored value."""

        pass
