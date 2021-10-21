import praw
import pandas as pd
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update(df):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("reddit").sheet1 
    data = sheet.get_all_records()  
    sheet.update([df.columns.values.tolist()] + df.values.tolist())


def scrape():
    posts = []

    id = "ROpOaQiBgUAsLw"
    key = "xQkoVMppm1pDAFJrNo2Dgr33ItW1yA"
    agent = "viz_scraper"

    reddit = praw.Reddit(client_id=id, client_secret=key, user_agent=agent)

    for submission in reddit.subreddit('all').hot(limit=100000):
        url = submission.url
        post = submission.selftext
        if ((" graph " in post or "viz" in post) and (url.endswith(('.jpg', '.png', '.gif', '.jpeg')))):
            print(url)
        # if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
        #     posts.append([str(submission.title), str(submission.score), str(submission.id), str(submission.subreddit), str(submission.url), str(submission.num_comments), str(submission.selftext), str(submission.created),])
    
    # posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    # update(posts); 

scrape()