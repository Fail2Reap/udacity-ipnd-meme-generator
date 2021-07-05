from abc import ABC, abstractmethod
from typing import List

from QuoteEngine.Models import QuoteModel


class IngestorInterface(ABC):
    """Interface superclass for ingestors."""
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Determines if the file is ingestable.

        Args:
            path (str): Path of file to ingest.

        Returns:
            bool: True if file is in valid ingestable extensions.
        """
        return path.split('.')[-1] in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Abstract file parsing method for subclasses.

        Args:
            path (str): Path of file to ingest.
        """
        pass
