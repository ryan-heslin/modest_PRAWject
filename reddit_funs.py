# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 09:50:15 2021

@author: heslinr1
"""

import praw
from praw.models import MoreComments
import textwrap
import functools as ft
import re
import os
from datetime import date
from colors import *

"""Initialize a Reddit instance after reading or importing a configuration file
for the API's environment variables."""
def config_reddit():
    env_vars = ["REDDIT_SCRIPT_USE", "REDDIT_SECRET", "APP_NAME",
            "REDDIT_USERNAME", "REDDIT_PASSWORD"]
    args = ["client_id", "client_secret", "user_agent", "username", "password"]
    mapping = dict(zip(args, [os.environ.get(var) for var in env_vars]))
    reddit = praw.Reddit(check_for_async = False, **mapping)
    return reddit


def format_comment(comment, indent = 0):
    """
    Extracts text of a Reddit comment and formats
    it for printing.

    Parameters
    ----------
    comment : praw.models.Comment
        isntance of praw Comment object.
    indent : int, optional
        Spaces to indent printed comment.
        The default is 0.

    Returns
    -------
    (string)
        Text of comment formatted for printing,
        wrapped and indented accordingly.

    """
    return "\n".join(
        textwrap.wrap(str(comment.author) +": " + 
        re.sub("\n", "", comment.body),
        initial_indent=" " * indent,
        subsequent_indent = " " * indent, width=80))


def trav_thread(thread, depth = 0, sep = "-" * 80):
    """
    Recursively traverses a comment_forest instance,
    printing all comments with indentation corresponding to 
    their position in the structure.

    Parameters
    ----------
    thread : praw.models.comment_forest
        comment_forest instance representing a Reddit
        comments thread
    depth : int, optional
        Nesting depth of current comment_forest object
        with regard to original. The default is 0, representing
        top-level comments. Intended to manage recursion; should
        not be modified by the user.
    sep : string, optional
        String to separate each displayed comment. The default is "-" * 80.

    Returns
    -------
    None.

    """
  
    for comment in thread:
        if not isinstance(comment, MoreComments):
            print(format_comment(comment, indent = depth * 2))
            print(sep)
            if hasattr(comment, "replies"):
                trav_thread(comment.replies, depth + 1) 
                

def scrape_top(subs, time_range = "day", n_posts = 5, sep = "-" * 80):
    """
    Extracts specified number of comments in time
    range from each subreddit in list and passes them
    to helper functions for printing to the terminal.

    Parameters
    ----------
    subs : (list)
        List of praw.models.Subreddit
    time_range : str, optional
        Time range for search. See documentation
        for praw.models.Subreddit top method for
        valid values. The default is "day".
    n_posts : int, optional
        Number of posts to display per subreddit.
        Effectively limited to 1,000 by praw's design.
        The default is 5.
    sep : str, optional
        String to separate each displayed comment. The default is "-" * 80.

    Returns
    -------
    None.

    """
    print(f"{bcolors.HEADER}Scraping top {n_posts} submission(s) for {os.environ['REDDIT_USERNAME']} on {date.today().strftime('%B %d, %Y')}{bcolors.ENDC}")
    for sub in subs:
        print(f"{bcolors.OKGREEN}r/{sub}")
        print(sep+"\n")
        for post in sub.top(limit = n_posts, time_filter = time_range):
            print(f"{bcolors.OKCYAN}{textwrap.wrap(str(post.author) + ': ' + post.title, width = len(sep)).pop()}{bcolors.ENDC}")
            print(sep)
            trav_thread(post.comments, sep = sep)
        print("\n")
        
def verify_sub(sub, reddit):
    try: 
        reddit.subreddits.search_by_name(sub, exact = True)
        return True
    except:
        return False

def list2subreddits(subs, reddit):
    """
    Given a list of subreddit names, returns a subreddits isntance containing
    those subreddits. Names of nonexistent subreddits are removed. 

    Parameters
    ----------
    subs : (list)
        A list of strings representing the names of subreddits.
    reddit (praw.Reddit)
        Instance of PRAW Reddit class

    Returns
    -------
    subs : (praw.subreddits)
        Subreddits instance containing valid subreddits passed to the function.
        If none are valid, None.

    """
   
    i =0
    while i < len(subs):
        try:
            subs[i] = reddit.subreddits.search_by_name(subs[i], exact = True).pop()
            i += 1 #Found subreddit, advance to next
        except:
            subs.pop(i) #Subreddit does not exist, remove from list
  
    if len(subs) == 0:
        subs = None
    return subs

def list2users(users, reddit):
    """
    Converts a list of strings representing usernames into
    list of Redditor instances, removing invalid usernames.

    Parameters
    ----------
    users : (list)
        List of reddit usernames
    reddit : (praw.Reddit)
        Instance of Praw Reddit class

    Returns
    -------
    users : (list)
        List of praw.models.Redditor isntances

    """
    i =0
    while i < len(users):
        try:
            users[i] = reddit.redditor(users[i]).comments.new(limit = None)
            i += 1 #Found user, advance to next
        except:
            users.pop(i) #User does not exist, remove from list
  
    if len(users) == 0:
        users = None
    return users

"""Not curerntly used"""
# From https://stackoverflow.com/questions/24912150/filter-a-list-using-a-lambda-that-raises-exceptions/24912901
def exclude_if_error(original, *args, **kwargs):
    try:
        original(*args, **kwargs)
        return True
    except:
        return False
        
    
def filter_transform(x, pred, transform):
    for element in x:
        if pred(element):
            yield(transform(element))
            
