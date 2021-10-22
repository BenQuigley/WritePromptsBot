# WritePromptsBot

This bot creates writing prompts from open source art and a wordlist and
tweets them out every day for your enjoyment.

On Twitter: [WritePromptsBot](https://twitter.com/WritePromptsBot)

To generate a writing prompt, clone the repository, and run the application in
test mode:

    git clone https://github.com/BenQuigley/WritePromptsBot.git
    cd WritePromptsBot
    pip install -r requirements.txt
    python main.py  --test

To run the application without test mode, you need the developer keys to a
Twitter bot. I store mine locally in `secret.py` as variables named
CONSUMER_KEY, CONSUMER_SECRET, KEY, and SECRET. If the bot cannot find
`secret.py`, it assumes that it's running on Heroku and tries to use those
variable names as keys to obtain the secrets from `os.environ` instead.

Example:

![](example.png "Example")
