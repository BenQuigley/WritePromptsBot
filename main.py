"""Main code for writing prompts Twitter bot."""

import json
import logging
import os
import random
import re
import sys
import time
import zipfile

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
ICONS_ZIP = os.path.join(STATIC_DIR, "lorc_icons/game-icons.net.svg.zip")
HTML_TEMPLATE = "templates/image.html"

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


def color_svg_image(svg_path: str, color: str) -> None:
    """Edit an SVG image to replace its background with the supplied color."""
    with open(svg_path) as infile:
        svg_contents = infile.readlines()
    with open(svg_path, "w") as outfile:
        for line in svg_contents:
            processed_line = re.sub('fill="#fff"', f'fill="{color}"', line)
            LOGGER.debug("Writing %s", processed_line)
            outfile.write(processed_line)


def gen_tweet_contents() -> str:
    """Placeholder."""
    return "Beep boop... {}".format(random_polite_word())


def generate_html(color: str, word: str, image: str) -> str:
    """Return HTML formatted with a given word and image."""
    with open(HTML_TEMPLATE) as infile:
        template = infile.read()
    return template % (color, word, image)


def main() -> None:
    """Main control flow function."""
    profanity.load_censor_words()  # Initialize the list of bad words
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
    api = tweepy.API(auth)

    LOGGER.info("Logged in successfully as {}".format(api.me().screen_name))

    while True:
        word = random_polite_word()
        tweet_contents = gen_tweet_contents()
        color = random.choice(COLORS)
        image = random_image()
        color_svg_image(image, color)
        html = generate_html(color, word, image)
        html_file = "index.html"
        with open(html_file, "w") as outfile:
            outfile.write(html)
        os.system(f"firefox {html_file}")
        if TEST_MODE:
            LOGGER.info(
                "Not tweeting, because test mode, but contents would be:"
            )
            LOGGER.info(tweet_contents)
        else:
            api.update_with_media("test.png", tweet_contents)
            LOGGER.info("Tweeted '%s'", tweet_contents)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
