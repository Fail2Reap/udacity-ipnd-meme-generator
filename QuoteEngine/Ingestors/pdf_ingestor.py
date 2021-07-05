import io
import subprocess
from typing import List

from QuoteEngine.ingestor_interface import IngestorInterface
from QuoteEngine.Models import QuoteModel


class PDFIngestor(IngestorInterface):
    """Subclass for ingesting pdf files."""
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Method for parsing ingested file.

        Args:
            path (str): Path to the file to ingest.
        """
        # STUDENT NOTE: There was no need to create temporary files.
        # By simply capturing the process output we can simply turn
        # this into an io object and work with it like a file in
        # memory.
        result = subprocess.run(
            ['pdftotext', '-layout', '-nopgbrk', path, '-'],
            capture_output=True,
            text=True
        )

        if not result.returncode:
            return [
                QuoteModel(*line.replace('"', "").rstrip('\n').split(" - "))
                for line in io.StringIO(result.stdout).readlines()
            ]

        raise Exception(result.stderr)
