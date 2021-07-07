from typing import List

from QuoteEngine.ingestor_interface import IngestorInterface
from QuoteEngine.Models import QuoteModel

from pandas import read_csv


class CSVIngestor(IngestorInterface):
    """Subclass for ingesting csv files."""
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Method for parsing ingested file.

        Args:
            path (str): Path to the file to ingest.
        """
        return [
            QuoteModel(row.body.replace('"', ""), row.author)
            for _, row in read_csv(path, header=0).iterrows()
        ]
