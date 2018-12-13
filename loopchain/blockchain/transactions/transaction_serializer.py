from abc import abstractmethod, ABC
from typing import TYPE_CHECKING
from ..hashing import build_hash_generator

if TYPE_CHECKING:
    from . import TransactionVersioner
    from .transaction import Transaction


class TransactionSerializer(ABC):
    _hash_salt = None

    def __init__(self, hash_generator_version: int):
        self._hash_generator = build_hash_generator(hash_generator_version, self._hash_salt)

    @abstractmethod
    def to_origin_data(self, tx: 'Transaction'):
        raise NotImplementedError

    @abstractmethod
    def to_raw_data(self, tx: 'Transaction'):
        raise NotImplementedError

    @abstractmethod
    def to_full_data(self, tx: 'Transaction'):
        raise NotImplementedError

    @abstractmethod
    def to_db_data(self, tx: 'Transaction'):
        raise NotImplementedError

    @abstractmethod
    def from_(self, tx_dumped: dict) -> 'Transaction':
        raise NotImplementedError

    @abstractmethod
    def get_hash(self, tx_dumped: dict) -> str:
        raise NotImplementedError

    @classmethod
    def new(cls, version: str, versioner: 'TransactionVersioner'):
        from . import genesis, v2, v3
        hash_generator_version = versioner.get_hash_generator_version(version)
        if version == genesis.version:
            return genesis.TransactionSerializer(hash_generator_version)
        elif version == v2.version:
            return v2.TransactionSerializer(hash_generator_version)
        elif version == v3.version:
            return v3.TransactionSerializer(hash_generator_version)

        raise RuntimeError(f"Not supported tx version({version})")
