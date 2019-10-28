import praw
from multiprocessing import Process

#### EDIT YOUR DETAILS  BELOW ####

# Your old account login details
old_username = ''
old_password = ''

# Your old account app details
old_user_agent = 'bot'
old_client_id = ''
old_client_secret = ''

# Your new account login details
new_username = ''
new_password = ''

# Your new account app details
new_user_agent = 'bot'
new_client_id = ''
new_client_secret = ''

# Copy options
copy_saved = False # set to True in order to copy all saved posts to the new account
copy_hidden = False # set to True in order to copy all hidden posts to the new account
copy_upvoted = False # set to True in order to copy all saved posts to the new account
copy_subscriptions = False # set to True in order to subscribe the new account to all subreddits the old
# account is subscribed to

#### DO NOT EDIT BELOW ####

old_reddit = praw.Reddit(
    client_id=old_client_id,
    client_secret=old_client_secret,
    user_agent=old_user_agent,
    username=old_username,
    password=old_password)


new_reddit = praw.Reddit(
    client_id=new_client_id,
    client_secret=new_client_secret,
    user_agent=new_user_agent,
    username=new_username,
    password=new_password)


def get_saved_total():
    saved_count = 0
    for saved in old_reddit.redditor(old_username).saved():
        saved_count += 1
    return saved_count


def get_hidden_total():
    hidden_count = 0
    for hidden in old_reddit.redditor(old_username).hidden():
        hidden_count += 1
    return hidden_count


def get_upvoted_total():
    upvoted_count = 0
    for upvoted in old_reddit.redditor(old_username).upvoted():
        upvoted_count += 1
    return upvoted_count


def get_subreddit_total():
    subscribed = list(old_reddit.user.subreddits(limit=None))
    return len(subscribed)


def start_copying_saved():
    print('Calculating number of saved posts, please wait...')
    saved_count = get_saved_total()
    print(f'Beginning copy of {saved_count} posts.')
    while saved_count > 0:
        for saved in reversed(list(old_reddit.redditor(old_username).saved())):
            try:
                saved_to_copy = new_reddit.submission(saved)
                saved_to_copy.save()
            except:
                saved_to_copy = new_reddit.comment(saved)
                saved_to_copy.save()
            saved_count -= 1
            print(f'{saved} copied. {saved_count} to go.')


def start_copying_hidden():
    print('Calculating number of hidden posts, please wait...')
    hidden_count = get_hidden_total()
    print(f'Beginning copy of {hidden_count} posts.')
    while hidden_count > 0:
        for hidden in reversed(list(old_reddit.redditor(old_username).hidden())):
            hidden_to_copy = new_reddit.submission(hidden)
            hidden_to_copy.hide()
            hidden_count -= 1
            print(f'{hidden} copied. {hidden_count} to go.')


def start_converting_upvoted_to_saved():
    print('Calculating number of upvoted posts, please wait...')
    upvoted_count = get_upvoted_total()
    print(f'Beginning conversion of {upvoted_count} posts.')
    while upvoted_count > 0:
        for upvoted in reversed(list(old_reddit.redditor(old_username).upvoted())):
            upvoted_to_convert = new_reddit.submission(upvoted)
            upvoted_to_convert.save()
            upvoted_count -= 1
            print(f'{upvoted} converted. {upvoted_count} to go.')


def start_resubbing():
    print('Calculating number of subreddits, please wait...')
    subreddit_count = get_subreddit_total()
    print(f'Beginning re subbing of {subreddit_count} subreddits.')
    while subreddit_count > 0:
        for subreddit in list(old_reddit.user.subreddits(limit=None)):
            new_reddit.subreddit(subreddit.display_name).subscribe()
            subreddit_count -= 1
            print(f'{subreddit} subscribbed to. {subreddit_count} to go.')


if __name__ == '__main__':
    if copy_saved:
        p1 = Process(target=start_copying_saved)
        p1.start()
    if copy_hidden:
        p2 = Process(target=start_copying_hidden)
        p2.start()
    if copy_upvoted:
        p3 = Process(target=start_converting_upvoted_to_saved)
        p3.start()
    if copy_subscriptions:
        p4 = Process(target=start_resubbing)
        p4.start()
