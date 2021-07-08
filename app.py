import os
import random
import tempfile
import requests

from flask.helpers import flash, url_for
from flask import Flask, render_template, request, redirect, \
                  send_from_directory

from MemeGenerator import MemeEngine
from QuoteEngine import Ingestor

app = Flask(__name__)
app.config['SECRET_KEY'] = \
    os.environ.get("SECRET_KEY", "4MCMg2*eDiI^Ui9zli57&8j0beGFDF9@")

meme = MemeEngine('./static/images')


def setup():
    """ Load all resources """

    quote_files = ['./static/DogQuotes/DogQuotesTXT.txt',
                   './static/DogQuotes/DogQuotesDOCX.docx',
                   './static/DogQuotes/DogQuotesPDF.pdf',
                   './static/DogQuotes/DogQuotesCSV.csv']
    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./static/photos/dog/"
    imgs = []
    for root, _, files in os.walk(images_path):
        imgs = [
            os.path.join(root, name)
            for name in files
            if name.split('.')[1].lower() in meme.image_extensions
        ]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # STUDENT NOTE: Enhanced the meme.html template so that if no image
    # is found it will instead display a placeholder image stored in
    # ./static/images/no_meme.png
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)

    return render_template(
        'meme.html',
        path=url_for('static', 
                     filename=f'images/{os.path.basename(path)}'))


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    data = request.form
    image_url = data.get('image_url')
    body = data.get('body')
    author = data.get('author')

    # STUDENT NOTE: I implemented some rudimentary form validation
    # to ensure that a user completes all fields. If not, it will
    # flash an error message. As part of this I also edited the
    # meme_form.html template to print any flash messages.
    if not image_url or not body or not author:
        flash("Please complete all fields and try again.", 'error')
        return redirect(url_for('meme_form'))

    respone = requests.get(image_url)

    # STUDENT NOTE: Another great place to use the tempfile lib,
    # and this time with delete=True so that the file gets deleted
    # automatically when closed.
    path = None
    try:
        image_path = tempfile.NamedTemporaryFile(
                prefix="srcimg-", suffix=".png", delete=True,
                dir=meme.output_dir)

        with open(image_path.name, 'wb') as f:
            f.write(respone.content)

        path = meme.make_meme(
                image_path, body, author)

    except Exception as e:
        flash(e, 'error')
        return redirect(url_for('meme_form'))

    finally:
        image_path.close()

    return render_template(
        'meme.html',
        path=url_for('static', 
                     filename=f'images/{os.path.basename(path)}'))


if __name__ == "__main__":
    app.run()
