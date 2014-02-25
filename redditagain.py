#!/usr/bin/env python

import sys
import time
import csv
import os
import getpass

import praw

USER_AGENT = 'RedditAgain by /u/karangoeluw // github: karan'


def print_dot():
    """Prints out a dot on the same line when called"""
    sys.stdout.write('. ')
    sys.stdout.flush()

def csv_file(fp, header):
    """Create or append a CSV file."""
    if os.path.exists(fp):
        f = open(fp, 'ab')
        writer = csv.writer(f)
    else:
        f = open(fp, 'wb')
        writer = csv.writer(f)
        writer.writerow(header)

    return f, writer

def format_time(created):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created))

# Ask the user for a decision. 'y' and 'Y' will evaluate to True, anything else will equate to False.
# A better implementation is welcome, it's just a quick-n-dirty slap-together job! -ChainsawPolice
def y_or_n(decision):
    if decision.lower=='y': return True
    else:                   return False


if __name__ == '__main__':
    print '>> Login to OLD account..'

    old_r = praw.Reddit(USER_AGENT)  # praw.Reddit
    old_r.login()

    print '\t>>Login successful..'
    old_user = old_r.user  # get a praw.objects.LoggedInRedditor object

    print 'Would you like to remove all your old comments? (y/n)'
    if y_or_n(raw_input('> ')) == True:
        print '>> Saving and editing all comments...'

        comment_file, comment_csv = csv_file(
            '{}_comments.csv'.format(old_user.name),
            ['Comment', "Posted on", "Thread"])

        with comment_file:
            removed = 1
            while removed > 0:  # keep going until everything is gone
                removed = 0
                for com in old_user.get_comments(limit=None):
                    link = com.submission.permalink.encode('utf-8')
                    body = com.body.encode('utf-8')
                    row = [body, format_time(com.created), link]
                    try:
                        comment_csv.writerow(row)
                        com.edit('.')
                        removed += 1
                        print_dot()
                    except Exception as e:
                        print 'Failed to store', link
                        print e
        print '\n\t>> Saved to {0}_comments.csv'.format(old_user.name)

    print 'Would you like to remove all your old submissions? (y/n)'
    if y_or_n(raw_input('> ')) == True:
        print '>> Saving and editing all submissions...'
        submission_header = ['Title', "Body/Link", "Created", "Karma"]
        submission_file, submission_csv = csv_file(
            '{}_submissions.csv'.format(old_user.name),
            submission_header)

        with submission_file:
            removed = 1
            while removed > 0:  # keep going until everything is gone
                removed = 0
                for sub in old_user.get_submitted(limit=None):
                    if sub.is_self:
                        submission = sub.selftext.encode('utf-8')
                    else:
                        submission = sub.url.encode('utf-8')
                    title = sub.title.encode('utf-8')
                    row = [title, submission, format_time(sub.created), sub.score]
                    try:
                        submission_csv.writerow(row)
                        sub.edit('.')
                        removed += 1
                        print_dot()
                    except Exception as e:
                        print 'Failed to store', submission
                        print e
        print '\n\t>> Saved to {0}_submissions.csv'.format(old_user.name)

    print '>> Preparing to migrate subscriptions.'
    subs = old_r.get_my_subreddits(limit=None)

    new_r = praw.Reddit(USER_AGENT)
    new_username = raw_input('>> Enter username of new account: ')

    while True:
        new_pass = getpass.getpass(
            '\t>> Enter password for `{}`: '.format(new_username))
        new_pass2 = getpass.getpass('\t>> Retype password to confirm: ')
        if new_pass != new_pass2:
            print 'Passwords do not match!'
        else:
            break

    # create the new account, if available
    if new_r.is_username_available(new_username):
        new_r.create_redditor(new_username, new_pass)

    new_r.login(new_username, new_pass)

    new_user = new_r.user  # get a praw.objects.LoggedInRedditor object
    print '\t>>Login successful..'

    print '>> Migrating subscriptions...'
    for sub in subs:
        new_r.get_subreddit(sub.display_name).subscribe()
        old_r.get_subreddit(sub.display_name).unsubscribe()
        print_dot()
    print '\n\t>> Done migrating.'

    print '>> Go to https://ssl.reddit.com/prefs/delete/',
    print 'to delete your old account.'