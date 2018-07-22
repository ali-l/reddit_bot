import yaml
import os
import praw
import random
from datetime import datetime
from reply_chooser import ReplyChooser
from lambda_quotes import LambdaQuotes
from word_filter import WordFilter

with open(f'{os.path.dirname(__file__)}/quotes.yml') as f:
    yaml_string_quotes = f.read()

string_quotes = yaml.load(yaml_string_quotes)

quotes = string_quotes + LambdaQuotes.all()

reddit = praw.Reddit('tyrion')

subreddit = 'freebots'
trigger = 'tyrion'

reply_chooser = ReplyChooser(random, quotes)
word_filter = WordFilter([trigger])

print('Listening for triggers...')

for comment in reddit.subreddit(subreddit).stream.comments(skip_existing=True):
    try:
        if trigger in comment.body.lower():
            reply = reply_chooser.reply(comment)

            if word_filter.is_blocked(reply):
                print(f'{datetime.utcnow()} - WordFilter blocked reply: {reply}')
                continue

            print(f'{datetime.utcnow()} - u/{comment.author.name} says: "{comment.body}". Replying with: "{reply}"')

            comment.reply(reply)
    except Exception as e:
        print(f'{datetime.utcnow()} - Exception: ', e)
        continue
