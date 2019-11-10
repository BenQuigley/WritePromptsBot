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


def random_image():
    """Return the name of a random image from the icon zip."""
    icons_zip = zipfile.ZipFile(ICONS_ZIP)
    icons_names = icons_zip.infolist()
    return random.choice(icons_names)


def tweet(twitter):
    """Send a new tweet to the Twitter account."""

    def gen_tweet_contents():
        """Placeholder."""
        return "Beep boop... {}".format(random_word())

    tweet_contents = gen_tweet_contents()
    while profanity.contains_profanity(tweet_contents):
        tweet_contents = gen_tweet_contents()
    twitter.update_status(tweet_contents)
    LOGGER.info("Tweeted '%s'", tweet_contents)


def main():
    """Main control flow function."""
    profanity.load_censor_words()  # Initialize the list of bad words
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
    api = tweepy.API(auth)

    LOGGER.info("Logged in successfully as {}".format(api.me().screen_name))

    while True:
        tweet(api)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
