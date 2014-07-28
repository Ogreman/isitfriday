from datetime import datetime, timedelta
from twittcher import SearchWatcher
from celery import Celery
from celery.task import periodic_task

import tweepy
import os


CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY  = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def tweet_back(tweet):
    api.update_status(
        status='{friday} RT @{tweet.username}: {tweet.text}'.format(
            friday='Yes' if datetime.now().weekday() == 4 else 'No',
            tweet=tweet,
        ),
        in_reply_to_status_id=tweet.link[tweet.link.rindex('/') + 1:]
    )


REDIS_URL = os.environ.get('REDISTOGO_URL', 'redis://localhost')
celery = Celery(__name__, broker=REDIS_URL)
bot = SearchWatcher("is it friday yet?", action=tweet_back)


@periodic_task(run_every=timedelta(minutes=5))
def check_tweets():
    bot.watch()