import praw
import pandas as pd
import sys
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials

from psaw import PushshiftAPI

from datetime import datetime, timedelta
import json
import os 


subreddits = [
    "worldnews",
    "news",
    "worldpolitics",
    "worldevents",
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



dates = [
    # Style dates to iterate over in the style of: "2021-12-01 00:00:00.000000"
]

def scrape():
    # posts_dict = {"Date": [], "Subreddit": [], "Title": [], "Post Text": [], "ID": [], "Score": [], "Total Comments": [], "Post URL": []}
    id = "ROpOaQiBgUAsLw"
    key = "xQkoVMppm1pDAFJrNo2Dgr33ItW1yA"
    agent = "viz_scraper"

    reddit = praw.Reddit(client_id=id, client_secret=key, user_agent=agent)

    api = PushshiftAPI()

    for date in dates:
        posts_dict = {"Date": [], "Subreddit": [], "Title": [], "Post Text": [], "ID": [], "Score": [], "Total Comments": [], "Post URL": []}
        start_date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        end_date_time_obj = start_date_time_obj+timedelta(days=1)
        for subreddit in subreddits:
            result = api.search_submissions(after=start_date_time_obj,before=end_date_time_obj,subreddit=subreddit)
            posts = list(result)
            for post in posts:
                if(post.url):
                    posts_dict["Date"].append(date)
                    posts_dict["Subreddit"].append(subreddit)
                    post_title = post.title[0:500]
                    if(len(post_title)>1000):
                        print(post_title)
                    posts_dict["Title"].append(post_title)
                    posts_dict["Post Text"].append("")
                    posts_dict["ID"].append(post.id)
                    posts_dict["Score"].append(post.score)
                    posts_dict["Total Comments"].append(post.num_comments)
                    posts_dict["Post URL"].append(post.url)
        update(posts_dict, date[0:10])


def update(df, dt_string):
    data = pd.DataFrame(df)
    credentials = {
        "type": "service_account",
        "project_id": "reddit-334418",
        "private_key_id": "dbc7344c3125d43531babfcee6706a230f58f675",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClgTpRDRNajJuJ\nsdw+QtludCube8RbOpc4Ea+w/w+rG+ll6dOnnG67b9mI6NWwty8GtsA1GZ0xIdJ+\nh+6NPqL5ZPp92J/eQnhIZNLC0r3QZxRs5eNRxkJnAzTHo085MAMWZbB0Vdwm4O5n\nebDYnV+gliktgm3vrhgwafC3ecR2NgwonuQ/Ib1DYNjpR/OTG8vD0fu2zFoFZRU/\nqRy1rsKwizzDJgh/ifQ9yRMZ90mOos9CMrcT+TSCi43o3Hqj/L7Bnsv5XZ3qi/sg\nPurakZJMQbsMZOUl0NqkMKONIZ5qY37Q896FtvqKJl1df1ntJMI31siyAGFfxaAa\nWlBk3JmZAgMBAAECggEABOACT+JNJOzzEscakB7uizulEAtBG49liuf5UZU4n6Tz\nQlQ+LsooHNhxTFvQh5FSWAFIpGMzMJJNeR88MJ7mIlUOHrFsrBl42LEOcoXOVmOZ\nw/5DPuSt/FQ7tHra2dVipC6txcZW0MSkztBUZV0J66IFQw/FL80tbYMTpD9UHJD0\nRv3Ktv5jx1FtaaZkME/zJnyejgCQ/rerVcGs1pjjU8zdMhtSvTa1s9sYAvlzu/8k\n1pefkLsZuVP/pO4GrVN7d5v3TjF8nv6Y7Ira//5h1ke7a9VaZjQwGskQbT2wji30\nxyTrw3B1WieHbnkgyAkZg9m63aDijGF4dVi+qIRrjQKBgQDY593pE8SSCLRYQ1gG\nKtU8+un+9bz/NuTJXBKLafzP2s0J43ZfSjn0QNxh6FBeVb+XaaxXVM6wh+NXAsh/\nyUolU0YIzsuRkIZIksw9Z9IyzKWzNvIVcQHYu6KH7fmwhKFMhotVEpqWoXD8cQvP\nI2KG6b7j5iCOkIU/HAhHQVUCBwKBgQDDVbKQtaWC1JdggffeHs7+PEqIQaQDqUMx\nWQtIasgkkXqMM7aFPJ9Z/sBXWVsCER6rbLTEhgkEjpOMpuwT3xc0Sr+8/PXRGsF9\nA+G3ZTB1I+X+E/ofH9z3eTHRqLBNKzyfdK0SfGIibjpK92coC6UxMfdAcPkD9G/9\nRhM2394fXwKBgDzxuSo6Aas+gt2h3mOtOUju/zxB856J3/KryhId74i/Y4j5vlK7\n2ljEuKdRzPMUiMaUTHYlQAXdyIS0JX2yIwElyrHC2PPHddOCW5yNRUQ8t/oI4DAi\nFnC9F8e1l8h/G4sS6qc2mPTl24cyhCzpNk/N8XK7QD6OYMIAsFrFAouVAoGBAINZ\nTAK88rfgBo6xtqBZLS2OEzw+j3Ca0AEN9GVU0JKudK50U6aSVkEo6eOSxXzFUE9L\ngN6plsTGrvckg5j1KeBS503I9+8NQ9Cx3IT6+TO72PsaKdXmEisjBtoJycuKaHB8\n/6hvlXm7j107sdUex40mITHnBbugEfJIvcDnlrCXAoGAcJmYYZB3IMn9/yEduBeu\nBIWM9IgOLBf/PIle15QSZmydPmTZAAFCHSa828qhrrvXPd/r1V2cJKmyihuNylCR\n1HBhn56BdMqvqXPfBFArL4fsgttEejBsZGD0bvsnLdBPiLg8SN9BD4w8qVVs+EpO\n1CvQnHOeuo6UctJX/snnRc0=\n-----END PRIVATE KEY-----\n",
        "client_email": "reddit@reddit-334418.iam.gserviceaccount.com",
        "client_id": "106682552318210817559",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/reddit%40reddit-334418.iam.gserviceaccount.com"
    } 
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("reddit_december")
    wk = sh.add_worksheet(title=dt_string, rows="1700", cols="15")
    set_with_dataframe(wk, data)
    print("Writing", dt_string, "to data.")


scrape()

    
