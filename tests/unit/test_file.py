from collections.abc import Generator
from tempfile import TemporaryFile
from typing import IO, override

import pytest

from pystores.file import FileStore, Serializer
from tests.utils.unit import BaseStoreTest, StoreLifespan, StoreLifespanBuilder


class FileStoreLifespan[T, R: (str, bytes)](StoreLifespan[T]):
    """Lifespan for FileStore."""

    def __init__(self, store: FileStore[T, R]) -> None:
        self._store = store

    @override
    async def enter(self) -> FileStore[T, R]:
        return self._store

    @override
    async def exit(self) -> None:
        return None


class FileStoreLifespanBuilder[T, R: (str, bytes)](StoreLifespanBuilder[T]):
    """Builder for FileStoreLifespan."""

    def __init__(self, file: IO[R], serializer: Serializer[T, R], default: T) -> None:
        self._file = file
        self._serializer = serializer
        self._default = default

    @override
    async def build(self) -> FileStoreLifespan[T, R]:
        return FileStoreLifespan(FileStore(self._file, self._serializer, self._default))


class IntSerializer(Serializer[int, str]):
    """Serializer for integers."""

    @override
    async def serialize(self, value: int) -> str:
        return str(value)

    @override
    async def deserialize(self, value: str) -> int:
        return int(value)


class TestFileStore(BaseStoreTest[int]):
    """Tests for FileStore."""

    @pytest.fixture
    def serializer(self) -> IntSerializer:
        """Return serializer for integers."""
        return IntSerializer()

    @pytest.fixture
    @override
    def builder(
        self, serializer: IntSerializer
    ) -> Generator[FileStoreLifespanBuilder[int, str]]:
        with TemporaryFile(mode="w+t") as file:
            yield FileStoreLifespanBuilder(file, serializer, 0)

    @pytest.fixture
    @override
    def value(self) -> int:
        return 1

    @pytest.fixture
    @override
    def other_value(self) -> int:
        return 2
