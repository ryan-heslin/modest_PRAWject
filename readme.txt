This project consists of several applications that use Reddit's PRAW API to
interact with the site. All use the argparse module to enable you to interact
with Reddit from the command line. autobrowse will extract the top comments in
your subscribed subreddits or others you specify; autopost lets you post text
from the command line; and autosearch searches or comments by regex, author,a
nd subreddit. For usage details, view the help for each program.

Each program works by configuring several environment variables needed to
initialize an insance of Reddit's PRAW class. Two of these, REDDIT_USERNAME
and REDDIT_PASSWORD, will be unique to each user. It is recommended you set
these environment variabes permanently in your .bash_profile (or equivalent,
depending on your system). If either or both are unset when the script is run,
you will be prompted to supply the missing variables at the command line.

Before running, be sure to run export PYTHONIOENCODING=UTF-8 in the terminal -
otherwise, it will not be able to render non-ASCII characters.

Happy Redditing!
