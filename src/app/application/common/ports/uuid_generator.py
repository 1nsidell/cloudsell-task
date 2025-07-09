from typing import Protocol


class UUIDGenerator(Protocol):
    """Интерфейс uuid генератора, чтобы прикладной слой не зависил от реализации."""

    def __call__(self) -> str: ...
