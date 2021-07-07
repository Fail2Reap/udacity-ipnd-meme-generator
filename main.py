import os
import random

from argparse import ArgumentParser

from MemeGenerator import MemeEngine
from QuoteEngine import Ingestor
from QuoteEngine.Models import QuoteModel


def generate_meme(img_path: str = None, body: str = None,
                  author: str = None) -> str:
    """Generates an images and returns a file path to where it's saved.

    Args:
        img_path (str, optional): Path to the source image or folder of images.
        Defaults to None.
        quote (str, optional): Quote to draw on the image. Defaults to None.
        author (str, optional): Author of the quote to draw on the image.
        Defaults to None.

    Raises:
        Exception: Raised if a quote body is provided without a quote author.

    Returns:
        str: File path to the generated image.
    """
    img = img_path
    meme = MemeEngine('./tmp')

    # STUDENT NOTE: Enhanced this to accept both a direct file path for the
    # image or a folder path to where one or more images are stored.
    if not img_path or (not os.path.isfile(img_path)
       and os.path.isdir(img_path)):
        imgs = []
        images = img_path
        if images is None:
            images = './static/photos/dog/'

        for root, _, files in os.walk(images):
            imgs = [
                os.path.join(root, name)
                for name in files
                if name.split('.')[1].lower() in meme.image_extensions
            ]

        if not imgs:
            raise Exception(
                f'No valid images ({", ".join(meme.image_extensions)})'
                f' were found in path: {img_path}')
        img = random.choice(imgs)

    elif not os.path.isfile(img_path) and not os.path.isdir(img_path):
        raise Exception(f'File or directory does not exist: {img_path}')

    if body is None:
        quote_files = ['./static/DogQuotes/DogQuotesTXT.txt',
                       './static/DogQuotes/DogQuotesDOCX.docx',
                       './static/DogQuotes/DogQuotesPDF.pdf',
                       './static/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))
        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author is required if a quote body is provided')
        quote = QuoteModel(body, author)

    img_path = meme.make_meme(img, quote.body, quote.author)
    return img_path


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Generates a meme and prints its file path.')
    parser.add_argument(
        '-p', '--path',
        help='file path of a specific image or folder path where one'
             ' or more images are stored')
    parser.add_argument(
        '-b', '--body',
        help='quote body to draw on the image')
    parser.add_argument(
        '-a', '--author',
        help='quote author to draw on the image')
    args = parser.parse_args()

    try:
        print(generate_meme(args.path, args.body, args.author))

    except Exception as e:
        print(f'ERROR: {e}')
