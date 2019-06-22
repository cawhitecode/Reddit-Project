import praw
import psycopg2
import datetime

#reddit api praw info
reddit = praw.Reddit(client_id='xxxxxxxxxxxxxxx', client_secret='xxxxxxxxxxxxxxx', user_agent='my user agent')

#object for submissions to index after this
class Subreddit(object):
    def __init__(self, title, subreddit, score, numb_comments, subscribers, time_rank):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.numb_comments = numb_comments
        self.subscribers = subscribers
        self.time_rank = time_rank

subreddit_info = []

#using reddit API to make an object or submission and indexing them, replacing ' for SQL inject
def reddit_pull():
    print('Reddit')
    rank = 0
    for submission in reddit.subreddit('all').hot(limit=25):
        rank +=1
        bad_title = str(submission.title)
        title = bad_title.replace("'", "%")
        title = (title[:200] + '..') if len(title) > 75 else title
        subreddit = str(submission.subreddit)
        score = int(submission.score)
        numb_comments = int(submission.num_comments)
        subscribers = int(submission.subreddit.subscribers)
        time = datetime.today()
        subreddit_info.append(Subreddit(title, subreddit, score, numb_comments, subscribers, rank, time))


#test to make sure objects are working
def test_data():
    for obj in subreddit_info:
        print("Title:", obj.title)
        print("/r", obj.subreddit)
        print("Score:", obj.score)
        print("Comments:", obj.numb_comments)
        print("Subscribers:",obj.subscribers)
        print("-----------")

#database connection, making of the table, and formatting data into SQL then injecting data
def sql_inject():
    connection = psycopg2.connect(user = "xxxxxxxxxxxxxxxxx", password = "xxxxxxxxx", host = "xxxxxxxxxxx", port = "xxxxxxx", database = "postgres")
    cursor = connection.cursor()
    print('Connected!')

    #this creates the table
    sql_command = """
    CREATE TABLE reddit_info_time_rank (
    title VARCHAR(225),
    subreddit VARCHAR(225),
    upvotes INTEGER,
    comments INTEGER,
    subscribers INTEGER,
    time VARCHAR(225) PRIMARY KEY,
    rank INTERGER);"""

    cursor.execute(sql_command)

    #this makes the object into a sql command to execute to database for each object
    for obj in subreddit_info:
        format_sql  = """INSERT INTO reddit_info_time_rank (title, subreddit, upvotes, comments, subscribers, time, rank)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');"""
        cursor.execute(format_sql.format(obj.title, obj.subreddit, obj.score, obj.numb_comments, obj.subscribers, obj.time, obj.rank))

        connection.commit()
        connection.close()
        print("----SUCCESS----")
        
#makes a function to call other functions.
def reddit_setup_all():
    reddit_pull()
    test_data()
    sql_inject()
    print('injection done')
    subreddit_info.clear()
    print('cleared subreddit_info')
    
#calls reddit setup to run
reddit_setup_all()
