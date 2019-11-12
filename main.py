"""Main code for writing prompts Twitter bot."""

import json
import logging
import os
import random
import time
import zipfile

import tweepy
from better_profanity import profanity

logging.basicConfig()
LOGGER = logging.getLogger("WritePromptsBot logger")
LOGGER.setLevel(logging.DEBUG)

INTERVAL = 60 * 60 * 8  # tweet every 8 hours
WORD_LIST = "static/english-words/words_dictionary.json"
ICONS_ZIP = "static/lorc_icons/game-icons.net.svg.zip"
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
    """Return the name of a random image from the icon zip."""
    icons_zip = zipfile.ZipFile(ICONS_ZIP)
    icons_names = icons_zip.infolist()
    return random.choice(icons_names)


def gen_tweet_contents() -> str:
    """Placeholder."""
    return "Beep boop... {}".format(random_polite_word())


def generate_html(word: str, image: str) -> str:
    """Return HTML formatted with a given word and image."""
    with open(HTML_TEMPLATE) as infile:
        template = infile.read()
    return template.format(word=word, image=image)


def main() -> None:
    """Main control flow function."""
    profanity.load_censor_words()  # Initialize the list of bad words
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
    api = tweepy.API(auth)

    LOGGER.info("Logged in successfully as {}".format(api.me().screen_name))

    while True:
        word = random_polite_word()
        html = generate_html(word, random_image().filename)
        html_file = "index.html"
        with open(html_file, "w") as outfile:
            outfile.write(html)
        os.system(f"firefox {html_file}")
        # twitter.update_status(tweet_contents)
        # LOGGER.info("Tweeted '%s'", tweet_contents)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
