
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 09:50:01 2021

@author: heslinr1
"""

from config import *
from reddit_funs import *
import sys
import argparse as ap

config_environ(app = "autopost")
reddit = config_reddit()

parser = ap.ArgumentParser(description = 'Specify arguments for Reddit post')
parser.add_argument('title', type = str, nargs = 1, help = "Title of submission")
parser.add_argument('selftext', type = str, nargs = 1, help = "Text to submit")
parser.add_argument('subreddit', type = str, nargs = 1, help = 
                    "Subreddit to submit to")
parser.add_argument('-r', '--resubmit',   action = 'store_true', 
                    help = 'Resubmit even if already submitted (default False)')
parser.add_argument('-n', '--nsfw',  action = 'store_true',
                    help  = 'Mark submission NSFW (default False)')
parser.add_argument('-s', '--spoiler',  action = 'store_true',
                    help = 'Spoiler submission (default False)')

parsed = parser.parse_args()
args = {k:  v.pop() if isinstance(v, list) else v for k, v in parsed.__dict__.items()}

# See https://www.reddit.com/r/redditdev/comments/68dhpm/praw_best_way_to_check_if_subreddit_exists_from/
try:
    reddit.subreddits.search_by_name(args['subreddit'], exact = True)
except:
    raise NameError
    print(f'r/{args["subreddit"]} does not exist')
    sys.exit(1)

print(f"Post to r/{args['subreddit']}:")
print(f"{args['title']}")
print(f"{args['selftext']}")
sub = args.pop("subreddit")
confirm = input("Press enter to confirm post, any other key to quit:\n")

if confirm == "":
    reddit.subreddit(sub).submit(**args)
else:
    print("Post canceled")
    sys.exit(0)