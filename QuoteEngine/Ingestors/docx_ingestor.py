from typing import List

from QuoteEngine.ingestor_interface import IngestorInterface
from QuoteEngine.Models import QuoteModel

from docx import Document


class DocxIngestor(IngestorInterface):
    """Subclass for ingesting docx files."""
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Method for parsing ingested file.

        Args:
            path (str): Path to the file to ingest.
        """
        return [
            QuoteModel(*para.text.replace('"', "").rstrip('\n').split(' - '))
            for para in Document(path).paragraphs
            if para.text
        ]
