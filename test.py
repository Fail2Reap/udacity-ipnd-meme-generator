from QuoteEngine import Ingestor

files = [
    './_data/DogQuotes/DogQuotesDOCX.docx',
    './_data/DogQuotes/DogQuotesCSV.csv',
    './_data/DogQuotes/DogQuotesPDF.pdf',
    './_data/DogQuotes/DogQuotesTXT.txt',
    './_data/DogQuotes/DogQuotesCSV.dda',
    './_data/DogQuotes/DogQuotesPDF.zip'
]

for file in files:
    try:
        quotes = Ingestor.parse(file)
        for quote in quotes:
            print(quote)

    except Exception as e:
        print(e)
