#!/usr/bin/env python

import sys

import praw

USER_AGENT = 'RedditAgain by @karangoeluw // github: thekarangoel'

def print_dot():
    sys.stdout.write('. ')
    sys.stdout.flush()
    print

if __name__ == '__main__':
    
    print '>> Login to OLD account..'
    
    old_r = praw.Reddit(USER_AGENT) # praw.Reddit
    old_r.login()
    
    print '\t>>Login successful..'
    old_user = old_r.user # get a praw.objects.LoggedInRedditor object
    
    print '>> Deleting all comments...'
    for com in old_user.get_comments(limit=None):
        com.delete()
        print_dot()
    
    print '>> Deleting all submissions...'
    for sub in old_user.get_submitted(limit=None):
        sub.delete()
        print_dot()
    
    print '>> Preparing to migrate subscriptions.'
    
    subs = old_r.get_my_subreddits(limit=None)
    
    new_r = praw.Reddit(USER_AGENT)
    new_username = raw_input('>> Enter username of new account to be registered.')
    new_pass = raw_input('\t>> Enter preferred password for %s' % new_username)
    
    new_r.create_redditor(new_username, new_pass) # create the new account
    
    new_r.login(new_username, new_pass)
    
    new_user = new_r.user # get a praw.objects.LoggedInRedditor object
    print '\t>>Login successful..'
    
    print '>> Migrating subscriptions...'
    for sub in subs:
        new_r.get_subreddit(sub.display_name).subscribe()
        old_r.get_subreddit(sub.display_name).unsubscribe()
        print_dot()
    
    print '>> Done migrating.'
    print '>> Go to https://ssl.reddit.com/prefs/delete/ to delete your old account.'