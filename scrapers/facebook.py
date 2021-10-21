from facebook_scraper import get_posts

image_urls = []

def scrape():
    # for post in get_posts(credentials = ["emma.lorraine.baker@gmail.com", "3143151244Emm@"], group="1499624933706213", pages=100):
    for post in get_posts("nintendo", pages=50):
        image_urls.append(post['images'])

scrape()
print(image_urls)