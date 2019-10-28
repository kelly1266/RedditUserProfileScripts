import praw
from multiprocessing import Process

#### EDIT YOUR DETAILS  BELOW ####

# Your login details
username = ''
password = ''

# Deletion options
limitation = None # None will delete ALL comments/submissions, 10 will delete recent 10 etc.
delete_comments = False # Set to False to not delete comments
delete_submissions = False # Set to False to not delete submissions


# Your app details
user_agent = 'bot'
client_id = ''
client_secret = ''

#### DO NOT EDIT BELOW ####


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password)


def get_comment_total():
    comment_count = 0
    for reply in reddit.redditor(username).comments.new(limit=limitation):
        comment_count += 1
    return comment_count


def get_submission_total():
    submission_count = 0
    for submission in reddit.redditor(username).submissions.new(limit=limitation):
        submission_count += 1
    return submission_count


def start_delete_comments():
    print('Calculating number of comments, please wait...')
    comment_count = get_comment_total() # 490
    print(f'Beginning deletion of {comment_count} comments.')
    while comment_count > 0:
        for comment in reddit.redditor(username).comments.new(limit=limitation):
            comment_to_delete = reddit.comment(comment)
            comment_to_delete.edit('This User\'s comments have been edited and deleted.')
            comment_to_delete.delete()
            comment_count -= 1
            print(f'{comment} deleted. {comment_count} to go.')


def start_delete_submissions():
    print('Calculating number of submissions, please wait...')
    submission_count = get_submission_total()
    print(f'Beginning deletion of {submission_count} submissions.')
    while submission_count > 0:
        for submission in reddit.redditor(username).submissions.new(limit=limitation):
            submission_to_delete = reddit.submission(submission)
            try:
                submission_to_delete.edit('This User\'s submissions have been edited and deleted.')
            except:
                print('Attempted to edit post and failed')
            submission_to_delete.delete()
            submission_count -= 1
            print(f'{submission} deleted. {submission_count} to go.')


if __name__ == '__main__':
    if delete_comments:
        p1 = Process(target=start_delete_comments)
        p1.start()
    if delete_submissions:
        p2 = Process(target=start_delete_submissions)
        p2.start()
