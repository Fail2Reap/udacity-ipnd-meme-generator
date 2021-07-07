import inspect

from pathlib import Path
from typing import List

from QuoteEngine.ingestor_interface import IngestorInterface
from QuoteEngine.Models import QuoteModel
from QuoteEngine import Ingestors


class Ingestor(IngestorInterface):
    """Generic file ingestor wrapper class."""
    # STUDENT NOTE: Somewhat proud of this little bit of magic here. Instead
    # of having to maintain a list of supported classes here, one simply
    # needs to include a new ingestor in the Ingestors module that inherits
    # from IngestorInterface and then edit the modules __init__.py file.
    # One less place to maintain code.
    ingestors = [
        ingestor[1]
        for ingestor in inspect.getmembers(Ingestors, inspect.isclass)
        if issubclass(ingestor[1], IngestorInterface)
    ]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Method for parsing ingested file.

        Args:
            path (str): Path to the file to ingest.
        """
        if Path(path).is_file():
            for ingestor in cls.ingestors:
                if ingestor.can_ingest(path):
                    return ingestor.parse(path)

            raise Exception(f'Unable to ingest file. No valid ingestor found'
                            f' for files of type: .{path.split(".")[-1]}')
        else:
            raise Exception('Unable to ingest file. File does not exist:'
                            f' {path}')
