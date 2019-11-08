"""Main code for writing prompts Twitter bot."""

import logging
import os

import tweepy

logging.basicConfig()
LOGGER = logging.getLogger("WritePromptsBot logger")
LOGGER.setLevel(logging.DEBUG)

try:
    from secret import CONSUMER_KEY, CONSUMER_SECRET, KEY, SECRET
except ImportError:
    CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
    KEY = os.environ.get("TWITTER_KEY")
    SECRET = os.environ.get("TWITTER_SECRET")


def main():
    """Main control flow function."""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(KEY, SECRET)
    api = tweepy.API(auth)

    LOGGER.info("Welcome {}".format(api.me().screen_name))


if __name__ == "__main__":
    main()
