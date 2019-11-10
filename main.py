"""Main code for writing prompts Twitter bot."""

import logging
import os
import time

import tweepy

logging.basicConfig()
LOGGER = logging.getLogger("WritePromptsBot logger")
LOGGER.setLevel(logging.DEBUG)

INTERVAL = 60 * 60 * 8  # tweet every 8 hours

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


def tweet(twitter):
    """Send a new tweet to the Twitter account."""
    twitter.update_status("Hello world!")


def main():
    """Main control flow function."""
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
    api = tweepy.API(auth)

    LOGGER.info("Logged in successfully as {}".format(api.me().screen_name))

    while True:
        tweet(api)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
