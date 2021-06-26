
# -*- coding: utf-8 -*-
from config import *
from reddit_funs import *
import argparse as ap
import sys
from colors import *

"""Extension of argparse.Action class"""
class SubredditsAction(ap.Action):
    
    """Overrides superclass method. 
    Converts list of string naming subreddits to list of reddit instances.
    If none are valid subreddits, exits with error."""
    def __call__(self, parser, namespace, argument_values, option_string = None):
        
        if( isinstance(argument_values, list)):
            argument_values = list2subreddits(subs = argument_values, reddit = reddit)
      
            if argument_values is None:
                print(f"{bcolors.FAIL}None of the specified subreddits exist {bcolors.ENDC}")
                sys.exit(1)
        
        setattr(namespace, "subreddits", argument_values)
    
config_environ(app = "autobrowse")
reddit = config_reddit()

parser = ap.ArgumentParser(description = "Specify parameters for Reddit browsing")
parser.add_argument("-n", "--nposts", type = int, default = 5, 
                   help = "Number of posts per subreddit to display")
parser.add_argument("subreddits", type = str, nargs = "*",
                    default = reddit.user.subreddits(), action = SubredditsAction, help = """ Names of 
                    subreddits to traverse. If not specified, subreddits to which
                    the user subscribes.""")
                    
parsed =parser.parse_args()
args = vars(parsed)

scrape_top(subs = args["subreddits"], n_posts = args["nposts"])
