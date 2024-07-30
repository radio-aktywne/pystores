from abc import abstractmethod
from os import SEEK_END
from typing import IO, Protocol

from pystores.base import Store


class FileNotReadableError(ValueError):
    """Raised when the file is not readable."""

    def __init__(self) -> None:
        super().__init__("File is not readable.")


class FileNotWritableError(ValueError):
    """Raised when the file is not writable."""

    def __init__(self) -> None:
        super().__init__("File is not writable.")


class FileNotSeekableError(ValueError):
    """Raised when the file is not seekable."""

    def __init__(self) -> None:
        super().__init__("File is not seekable.")


class Serializer[T, R](Protocol):
    """Serializer that serializes and deserializes the value."""

    @abstractmethod
    async def serialize(self, value: T) -> R:
        pass

    @abstractmethod
    async def deserialize(self, value: R) -> T:
        pass


class FileStore[T, R](Store[T]):
    """Store that stores the value in a file."""

    def __init__(self, file: IO[R], serializer: Serializer[T, R], default: T) -> None:
        if not file.readable():
            raise FileNotReadableError()

        if not file.writable():
            raise FileNotWritableError()

        if not file.seekable():
            raise FileNotSeekableError()

        self._file = file
        self._serializer = serializer
        self._default = default

    def _get_size(self) -> int:
        position = self._file.tell()
        self._file.seek(0, SEEK_END)
        size = self._file.tell()
        self._file.seek(position)
        return size

    async def get(self) -> T:
        if self._get_size() == 0:
            await self.set(self._default)

        self._file.seek(0)
        content = self._file.read()
        return await self._serializer.deserialize(content)

    async def set(self, value: T) -> None:
        content = await self._serializer.serialize(value)
        self._file.seek(0)
        self._file.truncate()
        self._file.write(content)
        self._file.flush()
