import praw
import psycopg2
import schedule
import time


reddit = praw.Reddit(client_id='xxxxxxxxx',
                     client_secret='xxxxxxxxxxxxxx',
                     user_agent='xxxxxxxxxxxxx')

#object to index the subreddit info and to recall later for SQL translation
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
    for submission in reddit.subreddit('all').hot(limit=25):
        bad_title = str(submission.title)
        title = bad_title.replace("'", "%")
        title = (title[:200] + '..') if len(title) > 75 else title
        subreddit = str(submission.subreddit)
        score = int(submission.score)
        numb_comments = int(submission.num_comments)
        subscribers = int(submission.subreddit.subscribers)
        subreddit_info.append(MyClass(title, subreddit, score, numb_comments, subscribers))

#this connects to the server and put the reddit info into a readable formart for sql
def sql_inject():
    connection = psycopg2.connect(user = "xxxxxxxxx", password = "xxxxxxxx", host = "xxxxxxxxxxxxx", port = "xxxxxxxxx", database = "postgres")
    cursor = connection.cursor()
    print('Connected!')
    
#this is where the magic happens for SQL convert
    for obj in subreddit_info:
        format_sql  = """INSERT INTO reddit_info (title, subreddit, upvotes, comments, subscribers)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');"""
        cursor.execute(format_sql.format(obj.title, obj.subreddit, obj.score, obj.numb_comments, obj.subscribers))

    connection.commit()
    print("----SUCCESS----")


#used to run program while giving a few clarifications to make sure program is working as intended for test
def reddit_all():
    reddit_pull()
    sql_inject()
    print('injection done')
    subreddit_info.clear()
    print('cleared subreddit_info')

#runs program every two hours or reddit_all to be more specific
schedule.every(2).hours.do(reddit_all)

while 1:
    schedule.run_pending()
    time.sleep(1)
