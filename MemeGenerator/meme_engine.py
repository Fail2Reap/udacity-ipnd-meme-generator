import os
import random
import tempfile

from PIL import Image, ImageFont, ImageDraw


class MemeEngine:
    """MemeEngine class that provides functionality to
    generate images with quotes."""

    image_extensions = ['png', 'jpeg', 'jpg']

    def __init__(self, output_dir: str):
        """Init function for the MemeEngine.

        Verifies the directory provided in 'output_dir' exists. If not
        it creates it.

        Args:
            output_dir (str): Output directory for the generated meme.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.output_dir = output_dir

    def make_meme(self, img_path: str, quote: str, author: str,
                  width: int = 500) -> str:
        """Creates a really dank meme and returns a file path to where
        it's saved.

        Args:
            img_path (str): Path to the source image.
            quote (str): Quote to draw on the image.
            author (str): Author of the quote to draw on the image.
            width (int, optional): Maximum width of the generated image.
            Defaults to 500.

        Returns:
            str: File path to the generated image.
        """

        img = Image.open(img_path)
        ratio = width/float(img.size[0])
        new_height = int(ratio*float(img.size[1]))
        img = img.resize((width, round(new_height)), Image.ANTIALIAS)

        draw = ImageDraw.Draw(img)
        quote_font = ImageFont.truetype(
                './static/fonts/OpenSans-Light.ttf', size=25)
        author_font = ImageFont.truetype(
                './static/fonts/OpenSans-Light.ttf', size=20)

        # STUDENT NOTE: Although "ensuring that text is drawn within
        # image bounds" wasn't really part of the rubrik, it posed an
        # interesting challenge. I solved this issue by calculating
        # the left-most bounds of quote and right-most bounds of
        # and author text and then iterating until it is no longer
        # out of bounds. If after 30 attempts it still wasn't possible
        # to draw the text within bounds, we then also start to reduce
        # the font size.
        draw_text_attempts = 0
        font_offset = 0

        while True:
            quote_length = draw.textsize(quote, font=quote_font) + \
                quote_font.getoffset(quote)
            quote_text_x = random.randint(5, width)
            quote_text_y = random.randint(5, new_height)
            quote_left_edge = quote_text_x
            quote_top_edge = quote_text_y

            author_length = draw.textsize(author, font=quote_font) + \
                author_font.getoffset(author)
            author_text_x = quote_text_x + quote_length[0] - 20
            author_text_y = quote_text_y + 40 - font_offset
            author_right_edge = author_text_x + author_length[0]
            author_bottom_edge = author_text_y + author_length[1]

            total_text_x = author_right_edge - quote_left_edge
            if total_text_x < width:
                if quote_left_edge > 5 \
                   and quote_top_edge > 5 \
                   and author_right_edge < width - 5 \
                   and author_bottom_edge < new_height - 5:

                    draw.text((quote_text_x, quote_text_y), f'"{quote}"',
                              font=quote_font, fill='white', stroke_width=1)
                    draw.text((author_text_x, author_text_y), f'- {author}',
                              font=author_font, fill='white', stroke_width=1)
                    break

            draw_text_attempts += 1
            if draw_text_attempts > 30:
                quote_font = ImageFont.truetype(
                    './static/fonts/OpenSans-Light.ttf', size=25-font_offset)
                author_font = ImageFont.truetype(
                    './static/fonts/OpenSans-Light.ttf', size=20-font_offset)
                font_offset += 1

        out_file = tempfile.NamedTemporaryFile(
            prefix="meme-", suffix=".png", delete=False, dir=self.output_dir)
        img.save(out_file.name, "PNG")
        return out_file.name
