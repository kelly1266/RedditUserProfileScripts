import praw
from multiprocessing import Process

#### EDIT YOUR DETAILS  BELOW ####

# Your new account login details
username = ''
password = ''

# Your new account app details
user_agent = 'bot'
client_id = ''
client_secret = ''

# Clear options
clear_saved = False # set to True to unsave all posts on this account
clear_hidden = False # set to True to unhide all posts on this account
clear_upvoted = False # set to True to attempt to remove upvote for all posts the account has upvoted
clear_subscriptions = False # set to True to unsubscribe from all subreddits this account is subscribed to

#### DO NOT EDIT BELOW ####

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password)


def get_saved_total():
    saved_count = 0
    for saved in reddit.redditor(username).saved():
        saved_count += 1
    return saved_count


def get_hidden_total():
    hidden_count = 0
    for hidden in reddit.redditor(username).hidden():
        hidden_count += 1
    return hidden_count


def get_upvoted_total():
    upvoted_count = 0
    for upvoted in reddit.redditor(username).upvoted():
        upvoted_count += 1
    return upvoted_count


def get_subreddit_total():
    subscribed = list(reddit.user.subreddits(limit=None))
    return len(subscribed)


def start_unsaving():
    print('Calculating number of saved posts, please wait...')
    saved_count = get_saved_total()
    print(f'Beginning clear of {saved_count} posts.')
    while saved_count > 0:
        for saved in reversed(list(reddit.redditor(username).saved())):
            try:
                saved_to_clear = reddit.submission(saved)
                saved_to_clear.unsave()
            except:
                saved_to_clear = reddit.comment(saved)
                saved_to_clear.unsave()
            saved_count -= 1
            print(f'{saved} unsaved. {saved_count} to go.')



def start_unhiding():
    print('Calculating number of hidden posts, please wait...')
    hidden_count = get_hidden_total()
    print(f'Beginning clear of {hidden_count} posts.')
    while hidden_count > 0:
        for hidden in reversed(list(reddit.redditor(username).hidden())):
            hidden_to_clear = reddit.submission(hidden)
            hidden_to_clear.unhide()
            hidden_count -= 1
            print(f'{hidden} unhidden. {hidden_count} to go.')


def start_clear_upvotes():
    print('Calculating number of upvoted posts, please wait...')
    upvoted_count = get_upvoted_total()
    print(f'Beginning conversion of {upvoted_count} posts.')
    while upvoted_count > 0:
        for upvoted in reversed(list(reddit.redditor(username).upvoted())):
            upvoted_to_clear = reddit.submission(upvoted)
            try:
                upvoted_to_clear.clear_vote()
            except:
                None
            upvoted_count -= 1
            print(f'{upvoted} cleared. {upvoted_count} to go.')


def start_unsubbing():
    print('Calculating number of subreddits, please wait...')
    subreddit_count = get_subreddit_total()
    print(f'Beginning un subbing of {subreddit_count} subreddits.')
    while subreddit_count > 0:
        for subreddit in list(reddit.user.subreddits(limit=None)):
            reddit.subreddit(subreddit.display_name).unsubscribe()
            subreddit_count -= 1
            print(f'{subreddit} unsubscribbed to. {subreddit_count} to go.')


if __name__ == '__main__':
    if clear_saved:
        p1 = Process(target=start_unsaving)
        p1.start()
    if clear_hidden:
        p2 = Process(target=start_unhiding)
        p2.start()
    if clear_upvoted:
        p3 = Process(target=start_clear_upvotes)
        p3.start()
    if clear_subscriptions:
        p4 = Process(target=start_unsubbing)
        p4.start()
