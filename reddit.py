import praw
from apscheduler.schedulers.blocking import BlockingScheduler
import psycopg2
#importing reddit api praw, psycopg2, and scheduler to repeat every 12 hours.

reddit = praw.Reddit(client_id='xxxxxxxxxxxxxxx',
                     client_secret='xxxxxxxxxxxxxxx',
                     user_agent='my user agent')

#object for submissions to index after this
class MyClass(object):
    def __init__(self, title, subreddit, score, numb_comments, subscribers):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.numb_comments = numb_comments
        self.subscribers = subscribers

subreddit_info = []
#using reddit API to make an object or submission and indexing them, replacing ' for SQL inject
    for submission in reddit.subreddit('all').hot(limit=20):
        bad_title = str(submission.title)
        title = bad_title.replace("'", "%")
        title = (title[:200] + '..') if len(title) > 75 else title
        subreddit = str(submission.subreddit)
        score = int(submission.score)
        numb_comments = int(submission.num_comments)
        subscribers = int(submission.subreddit.subscribers)
        subreddit_info.append(MyClass(title, subreddit, score, numb_comments, subscribers))

#test to make sure objects are working
for obj in subreddit_info:
    print("Title:", obj.title)
    print("/r", obj.subreddit)
    print("Score:", obj.score)
    print("Comments:", obj.numb_comments)
    print("Subscribers:",obj.subscribers)
    print("-----------")

#database connection

connection = psycopg2.connect(user = "xxxxxxx",
                                  password = "xxxxxxxx",
                                  host = "xxxxxxxxxxxx",
                                  port = "xxxxxxxxx",
                                  database = "postgres")

cursor = connection.cursor()

#comment out to avoid dropping table
#cursor.execute("""DROP TABLE reddit_info;""")

#this creates the table
sql_command = """
CREATE TABLE reddit_info (
title VARCHAR(225),
subreddit VARCHAR(225),
upvotes INTEGER PRIMARY KEY,
comments INTEGER,
subscribers INTEGER);"""

cursor.execute(sql_command)

#this makes the object into a sql command to execute to database for each object
for obj in subreddit_info:
    format_sql  = """INSERT INTO reddit_info (title, subreddit, upvotes, comments, subscribers)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');"""
    cursor.execute(format_sql.format(obj.title, obj.subreddit, obj.score, obj.numb_comments, obj.subscribers))


connection.commit()
connection.close()
print("----SUCCESS----")
