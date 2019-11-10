# Writing Prompts Bot

This bot creates writing prompts from open source art and a wordlist and
tweets them out every day for your enjoyment.

On Twitter: [WritePromptsBot](https://twitter.com/WritePromptsBot)

To run locally, you need the developer keys to a Twitter bot. I store mine
locally in `secret.py` as variables named CONSUMER_KEY, CONSUMER_SECRET, KEY,
and SECRET. If the bot cannot find `secret.py`, it assumes that it's running
on Heroku and tries to use those variable names as keys to obtain the secrets
from `os.environ` instead.

    git clone https://github.com/BenQuigley/WritePromptsBot.git
    cd WritePromptsBot
    virtualenv env
    pip install -r requirements.txt
    vi secret.py  # Add the keys
    python3 main.py
