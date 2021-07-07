from typing import List

from QuoteEngine.ingestor_interface import IngestorInterface
from QuoteEngine.Models import QuoteModel


class TextIngestor(IngestorInterface):
    """Subclass for ingesting txt files."""
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Method for parsing ingested file.

        Args:
            path (str): Path to the file to ingest.
        """
        with open(path, encoding="utf-8-sig") as file:
            return [
                QuoteModel(*line.replace('"', "").rstrip("\n").split(" - "))
                for line in file.readlines()
            ]
