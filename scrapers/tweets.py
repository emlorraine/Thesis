import json
from twitter import *


def get_url(text):
    if(("http") in text):
       index = text.index('http')
       return(text[index:])



def scrape():
    API_KEY = "qDKYw3tzEf8rUtxlODNO3esUi"
    API_SECRET = "JRTRBzYkJpyY515Gk7KnjeLub14fwIt9WWuiAKTe08BZ2IfIIC"
    ACCESS_TOKEN = "3363471245-Mtbc2WgNzG1nh1vhqhNrXCcGiGjxfWTJq20FeMX"
    ACCESS_TOKEN_SECRET = "VEQ0S9oV97gl7N33lZY5A3BfzuW5QMmSAnDwrUX1EaVPQ"
    t = Twitter(
        auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET))

    posts_dict = {"Date": [], "Page": [], "Title": [], "Post Text": [], "ID": [], "Total Comments": [], "Likes": [],  "Post URL": []}

    sources = [
        "nytimes",
        "washingtonpost",
        "cnn",
        "cnbc",
        "MSNBC",
        "fox",
        "usatoday",
        "Breitbart",
        "wsj",
        "npr",
        "politico",
        "bloomberg",
        "huffpost",
        "newyorker",
        "time"
    ]
    for source in sources: 
        user = t.statuses.user_timeline(screen_name=source)
        for entries in user:
            full_text = entries['text']
            link = get_url(full_text)
            if link:
                posts_dict["Date"].append(entries['created_at'])
                posts_dict["Page"].append(source)
                posts_dict["Title"].append("")
                posts_dict["Post Text"].append(entries['text'])
                posts_dict["ID"].append(entries['id'])
                posts_dict["Total Comments"].append(entries['retweet_count'])
                posts_dict["Likes"].append(entries['favorite_count'])
                posts_dict["Post URL"].append(link)
        print(posts_dict)
scrape() 
