from facebook_scraper import get_posts

for post in get_posts(credentials = ["emma.lorraine.baker@gmail.com", "3143151244Emm@"], group="1499624933706213", pages=100):
    print(post['text'][:50])