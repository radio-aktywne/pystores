from collections.abc import Generator
from tempfile import TemporaryFile
from typing import IO

import pytest

from pystores.file import FileStore, Serializer
from tests.utils.unit import BaseStoreTest, StoreLifespan, StoreLifespanBuilder


class FileStoreLifespan[T, R](StoreLifespan[T]):
    def __init__(self, store: FileStore[T, R]) -> None:
        self._store = store

    async def enter(self) -> FileStore[T, R]:
        return self._store

    async def exit(self) -> None:
        return None


class FileStoreLifespanBuilder[T, R](StoreLifespanBuilder[T]):
    def __init__(self, file: IO[R], serializer: Serializer[T, R], default: T) -> None:
        self._file = file
        self._serializer = serializer
        self._default = default

    async def build(self) -> FileStoreLifespan[T, R]:
        return FileStoreLifespan(FileStore(self._file, self._serializer, self._default))


class IntSerializer(Serializer[int, str]):
    async def serialize(self, value: int) -> str:
        return str(value)

    async def deserialize(self, value: str) -> int:
        return int(value)


class TestFileStore(BaseStoreTest[int]):
    @pytest.fixture()
    def serializer(self) -> IntSerializer:
        return IntSerializer()

    @pytest.fixture()
    def builder(
        self, serializer: IntSerializer
    ) -> Generator[FileStoreLifespanBuilder[int, str]]:
        with TemporaryFile(mode="w+t") as file:
            yield FileStoreLifespanBuilder(file, serializer, 0)

    @pytest.fixture()
    def value(self) -> int:
        return 1

    @pytest.fixture()
    def other_value(self) -> int:
        return 2
