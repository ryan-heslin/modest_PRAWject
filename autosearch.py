
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 11:08:35 2021

@author: heslinr1
"""

from config import *
from reddit_funs import *
import argparse as ap
from colors import *
import re
from math import inf
import itertools as it

"""Clever suggestion from Python discord user ConfusedReptile.
For an object y of this class, x in y is always True."""
class Universe:
    def __contains__(self, other):
        return True


class UserAction(ap.Action):
    
    """Overrides superclass method. Converts list of
    usernames to praw.models.Redditor instances. Exits with error if
    none are valid"""
    def __call__(self, parser, namespace, argument_values, option_string):
        argument_values = list2users(users = argument_values, reddit = reddit)
      
        if len(argument_values) == 0:
            print(f"{bcolors.FAIL}None of the specified Reddit users exist {bcolors.ENDC}")
            sys.exit(1)
        setattr(namespace, "users", argument_values)
        
class QueryAction(ap.Action):
    """Overrides superclass method. Verifies that a string passed to query is a valid
    regular expression."""
    def __call__(self, parser, namespace, argument_values, option_string = None):
        argument_values = argument_values.pop()
        try: 
             re.compile(argument_values)
        except re.error:
                print(f"{bcolors.FAIL}Bad regex pattern: {pattern} {bcolors.ENDC}")
                sys.exit(1)
        setattr(namespace, "query", argument_values)

class SubredditsAction(ap.Action):
    """Overrides superclass method. Finds valid subreddits
    names in a list and converts them to praw.models.Subreddit
    instances. If none are valid, exits with error."""
    def __call__(self, parser, namespace, argument_values, option_string):
        argument_values = list(filter(lambda x: verify_sub(x, reddit), argument_values))
        if not argument_values:
            print(f"{bcolors.FAIL}None of the specified subreddits exist {bcolors.ENDC}")
            sys.exit(1)
        setattr(namespace, "subreddits", argument_values)



config_environ(app = "autosearch")
reddit = config_reddit()

parser = ap.ArgumentParser(description = """Specify search parameters for comments
                           """)
parser.add_argument("query", action = QueryAction, nargs = 1, type = str, help = """Regular expression
                    (not quoted) against which comments are matched""")
parser.add_argument("-m", "--min_score", type = int, help = """Minimum karma score
                of comments to search""", default = -inf)
parser.add_argument("-s", "--subreddits", default = Universe(), nargs = "*",
                    action = SubredditsAction, help = """Subreddits to 
                search for""")
group =parser.add_mutually_exclusive_group()
group.add_argument("-u", "--users", default = list2users(users = [os.environ["REDDIT_USERNAME"]], reddit = reddit),
                nargs = "*", action = UserAction,
                help = """Reddit user whose comments to search. If omitted,
                the user stored in the REDDIT_USERNAME environment variable
                (which should be the user of this program). Cannot be invoked
                alongside --delete""")
group.add_argument("-d", "--delete", action = "store_true", 
                help = """Mark posts for deletion. Cannot be invoked alongside
                --users""")
                
parsed = parser.parse_args()
args = vars(parsed)

def filter_comment(comment, subreddits, min_score, query):
    ops = ["comment.subreddit in subreddits", "comment.score > min_score",
           "re.search(query, comment.body) is not None"]
    for op in ops:
        if not eval(op):
            return False
    return True
    
filter_args = {k : v for k, v in args.items() if k in ("subreddits", "min_score", "query")}
comments = list(filter(lambda x: filter_comment(comment = x, **filter_args), it.chain.from_iterable(args["users"])))
    
print(f"Search returned {len(comments)} comment(s):\n")
for comment in comments:
    print(comment.created_utc)
    print(format_comment(comment))
    print("-" * 80)

if(args["delete"]):
    confirm = input("Comments marked for deletion. Press Enter to confirm, any other key to cancel\n")
    
    if confirm =="":
        for comment in comments:
            comment.delete()
            print(f"All comments deleted")
    else:
        print("Deletion canceled")

