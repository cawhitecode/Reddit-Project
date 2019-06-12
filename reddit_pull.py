import praw
import psycopg2
import schedule
import time


reddit = praw.Reddit(client_id='xxxxxxxxx',
                     client_secret='xxxxxxxxxxxxxx',
                     user_agent='xxxxxxxxxxxxx')

#object for submissions to index after this
class MyClass(object):
    def __init__(self, title, subreddit, score, numb_comments, subscribers):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.numb_comments = numb_comments
        self.subscribers = subscribers

subreddit_info = []
#using reddit API to make an object or submission and indexing them
def reddit_pull():
    print('Reddit')
    for submission in reddit.subreddit('all').hot(limit=20):
        title = str(submission.title)
        subreddit = str(submission.subreddit)
        score = int(submission.score)
        numb_comments = int(submission.num_comments)
        subscribers = int(submission.subreddit.subscribers)
        subreddit_info.append(MyClass(title, subreddit, score, numb_comments, subscribers))

connection = psycopg2.connect(user = "xxxxxxxxxxx",
                              password = "xxxxxxxxxx",
                              host = "xxxxxxxxxxxxx",
                              port = "xxxxxxxxx",
                              database = "postgres")
cursor = connection.cursor()
print('Connected!')

def sql_inject():
    for obj in subreddit_info:
        format_sql  = """INSERT INTO reddit_info (title, subreddit, upvotes, comments, subscribers)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');"""
        cursor.execute(format_sql.format(obj.title, obj.subreddit, obj.score, obj.numb_comments, obj.subscribers))

def commit_sql():
    connection.commit()
    connection.close()
    print("----SUCCESS----")
#calls each function to do every 4 hours. I.e. pull top 20 of reddit, every 4 hours.
schedule.every(4).hour.do(reddit_pull)
schedule.every(4).hour.do(sql_inject)
schedule.every(4).hour.do(commit_sql)

while 1:
    schedule.run_pending()
    time.sleep(1)
