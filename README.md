# WritePromptsBot

This bot creates writing prompts from open source art and a wordlist and tweets them out every day
for your enjoyment.

## Using the Heroku Scheduler

These days, I mostly use this app as an example of how to take a program you've written, and run the
program automatically on a recurring basis, using the Heroku scheduler. Here is how to do that:

1. [Make a Heroku app](https://devcenter.heroku.com/articles/creating-apps) (there is a free tier at
   the time of this writing that works perfectly well for most scripting purposes), using whatever
   language (that Heroku supports) you like. Deploy the app to Heroku.
2. Determine the bash command to run your program. WritePromptsBot is a Python script written in the
   file [main.py](https://github.com/BenQuigley/WritePromptsBot/blob/master/main.py), so its run
   command is `python3 main.py`.
3. Use [these instructions](https://devcenter.heroku.com/articles/scheduler) to add the Heroku
   Scheduler add-on to your app (also free at the time of this writing).
4. Go to your [Heroku Dashboard](https://dashboard.heroku.com). Click Apps, then find your app.
   Click the "Resources" tab, then click "Heroku Scheduler" to open your scheduler configuration.
   Click "Add Job" to schedule your event. Heroku will prompt you to enter the timing for when the
   command should run, and what command it should use to run your code (see #2). When you are done,
   click "Save Job."

That's it!

## About WritePromptsBot

Visit the app on Twitter: [WritePromptsBot](https://twitter.com/WritePromptsBot)

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
