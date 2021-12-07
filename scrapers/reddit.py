import praw
import pandas as pd
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

subreddits = [
    "worldnews",
    "news",
    "worldpolitics",
    "worldevents",
    "business",
    "Economics",
    "politics",
    "uspolitics",
    "AmericanPolitics",
    "AmericanGovernment",
    "Libertarian",
    "socialism",
    "progressive",
    "conservative",
    "democrats",
    "Liberal",
    "Republican",
    "LibertarianLeft"
]

def update(df):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("reddit").sheet1 
    data = sheet.get_all_records()  
    sheet.update([df.columns.values.tolist()] + df.values.tolist())


def scrape():
    posts_dict = {"Date": [], "Subreddit": [], "Title": [], "Post Text": [], "ID": [], "Score": [], "Total Comments": [], "Post URL": []}

    id = "ROpOaQiBgUAsLw"
    key = "xQkoVMppm1pDAFJrNo2Dgr33ItW1yA"
    agent = "viz_scraper"

    reddit = praw.Reddit(client_id=id, client_secret=key, user_agent=agent)

    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).hot(limit=100):
            posts_dict["Date"].append(datetime.today().strftime('%Y-%m-%d'))
            posts_dict["Subreddit"].append(subreddit)
            posts_dict["Title"].append(submission.title)
            posts_dict["Post Text"].append(submission.selftext)
            posts_dict["ID"].append(submission.id)
            posts_dict["Score"].append(submission.score)
            posts_dict["Total Comments"].append(submission.num_comments)
            posts_dict["Post URL"].append(submission.url)
    
    posts = pd.DataFrame(posts_dict)
    print(posts)
    # posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    # update(posts); 

scrape()