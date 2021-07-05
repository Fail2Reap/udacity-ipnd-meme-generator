class QuoteModel:
    """Class to encapsulate imported quotes."""

    def __init__(self, body: str = '', author: str = '') -> None:
        self.body = str(body)
        self.author = str(author)

    def __str__(self) -> str:
        return f'"{self.body}" - {self.author}'

    def __repr__(self) -> str:
        return f'<"{self.author}", "{self.body}">'
