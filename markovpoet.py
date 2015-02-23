#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
# markovpoet.py
#   -- generate (bad, random) poetry
#
# Usage:
#
# markovepoet.py POET [options]
#
# POET:
#  Lovecraft
#  Shakespeare
#
# Options:
# --form [haiku|free_verse]  the form of poem to compose
# --post                     post the haiku to twitter
#

__author__ = 'Greg Boyington (@evilchili)'
__copyright__ = 'Copyleft (k) YOLD 3180. All Fail Disfnordia'
__license__ = 'FNORD'
__version__ = '1.0.0'

import argparse
import tweepy
from poet import Poet


def tweet(text):
    """
    Tweet a poem.
    """
    from twitter_auth import credentials
    auth = tweepy.OAuthHandler(
        credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
    auth.set_access_token(credentials.ACCESS_KEY, credentials.ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(text)


def main():
    parser = argparse.ArgumentParser(description='compose some (bad, random) poetry')
    parser.add_argument('-t', '--tweet', dest='tweet', help='tweet the poem', action='store_true')
    parser.add_argument('-s', '--source', dest='source', required=True, help='path to corpus text')
    parser.add_argument('-f', '--form', dest='form',
                        help='poetic form to compose', choices=('haiku', 'free_verse'))
    options = parser.parse_args()

    poet = Poet(corpus=options.source)
    poem = poet.compose(options.form)
    print poem
    print len(poem)

    # optionally, tweet the review.
    if options.tweet:
        print "Would tweet."
        # tweet(tweet)


if __name__ == '__main__':
    main()
