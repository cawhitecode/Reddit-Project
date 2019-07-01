SELECT subreddit, avg(upvotes), avg(comments), avg(upvotes)/avg(comments) FROM reddit_info
GROUP BY subreddit;