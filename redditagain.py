#!/usr/bin/env python

import sys

import praw

USER_AGENT = 'RedditAgain by @karangoeluw // github: thekarangoel'

if __name__ == '__main__':
    
    print '>> Login to OLD account..'
    
    r = praw.Reddit(USER_AGENT)
    r.login()
    
    print '\t>>Login successful..'
    old_user = r.user # get a praw.objects.Redditor object
    
    print '>> Deleting all comments...'
    for com in old_user.get_comments(limit=None):
        com.delete()
        sys.stdout.write('. ')
        sys.stdout.flush()
    
    
    print '>> Deleting all submissions...'
    for sub in old_user.get_submitted(limit=None):
        sub.delete()
        sys.stdout.write('. ')
        sys.stdout.flush()
    
    print '>> Preparing to migrate subscriptions.'
    
    subs = r.get_my_subreddits(limit=None)
    
    r2 = praw.Reddit(USER_AGENT)
    new_username = raw_input('>> Enter username of new account to be registered.')
    new_pass = raw_input('\t>> Enter preferred password for %s' % new_username)
    
    r2.create_redditor(new_username, new_pass) # create the new account
    
    r2.login(new_username, new_pass)
    
    new_user = r2.user # get a praw.objects.Redditor object
    print '\t>>Login successful..'
    
    print '>> Migrating subscriptions...'
    for sub in subs:
        r2.get_subreddit(sub.display_name).subscribe()
        r.get_subreddit(sub.display_name).unsubscribe()
        sys.stdout.write('. ')
        sys.stdout.flush()
    
    print '>> Done migrating. Deleting old user.'