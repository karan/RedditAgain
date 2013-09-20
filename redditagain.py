#!/usr/bin/env python

import sys
import time
import csv

import praw

USER_AGENT = 'RedditAgain by @karangoeluw // github: thekarangoel'

def print_dot():
    """Prints out a dot on the same line when called"""
    sys.stdout.write('. ')
    sys.stdout.flush()

def main():
    print '>> Login to OLD account..'

    old_r = praw.Reddit(USER_AGENT) # praw.Reddit
    old_r.login()

    print '\t>>Login successful..'
    old_user = old_r.user # get a praw.objects.LoggedInRedditor object

    print '>> Saving and Deleting all comments...'
    comment_file = csv.writer(open('%s_comments.csv' % old_user.name, 'wb'))
    comment_file.writerow(['Comment', "Posted on", "Thread"]) # header

    for com in old_user.get_comments(limit=None):
        comment_file.writerow([com.body,
                               time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(com.created)),
                               com.submission.permalink])
        com.delete()
        print_dot()
    comment_file.close()
    print '\n\t>> Saved to {0}_comments.csv'.format(old_user.name)

    print '>> Saving and Deleting all submissions...'
    submission_file = csv.writer(open('%s_submissions.csv' % old_user.name, 'wb'))
    submission_file.writerow(['Title', "Body/Link", "Created", "Karma"]) # header

    for sub in old_user.get_submitted(limit=None):
        submission_file.writerow([sub.title,
                                  sub.selftext if sub.is_self else sub.url,
                                  time.strftime('%Y-%m-%d %H:%M:%S',
                                                time.localtime(sub.created)),
                                  sub.score])
        sub.delete()
        print_dot()
    print '\n\t>> Saved to {0}_submissions.csv'.format(old_user.name)

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


if __name__ == '__main__':
    main()
