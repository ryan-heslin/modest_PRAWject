# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 09:58:53 2021

@author: heslinr1
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 09:37:57 2021

@author: heslinr1
"""

import os
import sys
from colors import *

def config_environ(app, username, password):
    os.environ["REDDIT_USERNAME"] = username
    os.environ["REDDIT_PASSWORD"] = password
    mapping = { "autobrowse" : {"APP_NAME" : "autobrowse", "REDDIT_SCRIPT_USE" :
                               "2EffsaZL9_-Jcw", "REDDIT_SECRET" : "rrXsNgrHNz9yzMzVLz5LXkIsNAIrig"},
           "autopost" : {"APP_NAME" : "autopost", 
                            "REDDIT_SCRIPT_USE" : "pQJgoy6tlCTHfA",
                            "REDDIT_SECRET" : "Lk-fWymUEprNta_CwJTksSIJS2V3xw"},
           "autosearch": {"APP_NAME" : "autosearch", "REDDIT_SCRIPT_USE": "YbvLJzmXIFWEWw",
                          "REDDIT_SECRET": "6ezoLhJRSE8S-E9hP5zyEY-Z4B1AMw"}}
    try:
        di = mapping[app]
    except KeyError:
        print(f"{bcolors.FAIL}{app} is not a valid app {bcolors.ENDC}")
        sys.exit(1)
    os.environ = {**os.environ, **di}
   