from uuid import uuid4

from app.application.common.ports.uuid_generator import UUIDGenerator


class UUIDGeneratorImpl(UUIDGenerator):
    def __call__(self) -> str:
        return str(uuid4())
