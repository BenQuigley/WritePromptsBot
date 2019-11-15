"""Main code for writing prompts Twitter bot."""

import json
import logging
import os
import random
import re
import sys
import time
import zipfile

from PIL import Image, ImageDraw, ImageFont

import tweepy
from better_profanity import profanity
from colors import COLORS

TEST_MODE = any(val in sys.argv[1:] for val in ("-t", "--test"))

logging.basicConfig()
LOGGER = logging.getLogger("WritePromptsBot logger")
LOGGER.setLevel(logging.INFO)

INTERVAL = 60 * 60 * 8  # tweet every 8 hours
STATIC_DIR = "static"
WORD_LIST = os.path.join(STATIC_DIR, "english-words/words_dictionary.json")
ICONS_ZIP = os.path.join(STATIC_DIR, "lorc_icons/game-icons.net.png.zip")
HTML_TEMPLATE = "templates/image.html"
HTML_FILENAME = "writing_prompt.html"
IMAGE_FILENAME = "writing_prompt.png"
IMAGE_FONT = (
    "static/fonts/Glacial Indifference Desktop Family OTF/"
    "GlacialIndifference-Regular.otf"
)

try:
    from secret import (
        TWITTER_CONSUMER_KEY,
        TWITTER_CONSUMER_SECRET,
        TWITTER_KEY,
        TWITTER_SECRET,
    )
except ImportError:
    TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
    TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
    TWITTER_KEY = os.environ.get("TWITTER_KEY")
    TWITTER_SECRET = os.environ.get("TWITTER_SECRET")


def random_word():
    """Return a random word from the word list."""
    # Loading from JSON for better performance.
    with open(WORD_LIST) as infile:
        words = tuple(json.loads(infile.read()).keys())
        return random.choice(words)


def random_polite_word():
    """Return a random non-profane word from the word list."""
    word = random_word()
    while profanity.contains_profanity(word):
        word = random_word()
    return word


def random_image() -> str:
    """Extract a random image from the icon zip, and returns its name."""
    icons_zip = zipfile.ZipFile(ICONS_ZIP)
    icons_names = icons_zip.infolist()
    icon = random.choice(icons_names)
    image_name = os.path.join(STATIC_DIR, icon.filename)
    icons_zip.extract(icon, STATIC_DIR)
    LOGGER.info(f"Using image: {image_name}")
    return image_name


def gen_tweet_contents(word: str) -> str:
    """Placeholder."""
    return "Beep boop... {}".format(word)


def generate_html(color: str, word: str, image: str) -> str:
    """Return HTML formatted with a given word and image."""
    # Nice to have: render this as a homepage using Flask
    with open(HTML_TEMPLATE) as infile:
        template = infile.read()
    return template % (color, word, image)


def generate_html_file(*args) -> None:
    """Create HTML formatted with a given word and image.

    :return: The HTML file's filename.
    """
    html = generate_html(*args)  # pylint: disable=no-value-for-parameter
    with open(HTML_FILENAME, "w") as outfile:
        outfile.write(html)


def center_item(context_width: int, item_width: int) -> int:
    """Return the start point to place an item centered in a context."""
    assert context_width > item_width
    return int((context_width - item_width) / 2)


def generate_formatted_image(color: str, word: str, icon_image: str) -> None:
    """Create an image formatted with a given word and image.

    :return: The image's filename.
    """
    image_dims = (1476, 772)
    image = Image.new("RGBA", image_dims, color=color)
    # Load the font and draw the word.
    image_font = ImageFont.truetype(IMAGE_FONT, 130)
    draw = ImageDraw.Draw(image)
    # Center the text on the image.
    width, _height = draw.textsize(word, font=image_font)
    draw.text(
        (center_item(image_dims[0], width), 35),
        word,
        fill=(0, 0, 0),
        font=image_font,
    )
    # Open the SVG file, and stamp it onto the formatted image.
    icon = Image.open(icon_image).convert("RGBA")
    image.paste(
        icon, (center_item(image_dims[0], icon.width), 205), mask=icon
    )
    image.save(IMAGE_FILENAME)


def main() -> None:
    """Main control flow function."""
    profanity.load_censor_words()  # Initialize the list of bad words
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
    api = tweepy.API(auth)

    LOGGER.info("Logged in successfully as {}".format(api.me().screen_name))

    while True:
        word = random_polite_word()
        text = f"{word}!"
        tweet_contents = gen_tweet_contents(word)
        color = random.choice(COLORS)
        image = random_image()
        generate_html_file(color, text, image)
        generate_formatted_image(color, text, image)
        if TEST_MODE:
            LOGGER.info(
                "Not tweeting, because test mode, but contents would be:"
            )
            LOGGER.info(tweet_contents)
            os.system(f"xdg-open {IMAGE_FILENAME} &")
        else:
            api.update_with_media(IMAGE_FILENAME, tweet_contents)
            LOGGER.info("Tweeted '%s'", tweet_contents)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
