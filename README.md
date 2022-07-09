# Thesis

Accepted thesis can be downloaded via WUSTL Open Scholarship [here](https://openscholarship.wustl.edu/eng_etds/707/). 

## Repo Structure:

- `📂all_data`: CSVs of all data scraped by month
- `📜viz_data.csv`: CSV of visualizations scraped with complexity anaylsis
- `📂imgs`: PNGs of visualizations scraped sorted by type
- `📂process_viz/access.py`: Helper to read/write to Google Sheets
- `📂process_viz/strainer.py`: Helper to filter and export records in  sheet
- `📂process_viz/urls/spiders/urlspider`: Engine to scrape Reddit and then load/inspect/scrape each url

```
📦src
 ┣ 📂all_data
 ┣ 📜viz_data.csv
 ┣ 📂imgs
 ┃ ┣ 📂area
 ┃ ┣ 📂bar
 ┃ ┣ 📂bubble
 ┃ ┣ 📂gauge
 ┃ ┣ 📂inforgraphic
 ┃ ┣ 📂line
 ┃ ┣ 📂map
 ┃ ┣ 📂network
 ┃ ┣ 📂pie
 ┃ ┣ 📂scatter
 ┃ ┣ 📂system
 ┃ ┣ 📂timeline
 ┃ ┣ 📂treemap
 ┃ ┣ 📂waffle
 ┣ 📂process_viz
 ┃ ┣ 📂output_manual_focus
 ┃ ┣ 📂output_page_screenshots
 ┃ ┣ 📜access.py
 ┃ ┣ 📜bitmap.py
 ┃ ┣ 📜density.py
 ┃ ┗ 📜strainer.py
 ┗ 📂scraper
 ┃ ┣ 📂urls
 ┃ ┃ ┣ 📂aquarium
 ┃ ┃ ┣ 📂output_screenshots
 ┃ ┃ ┣ 📂urls
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜items.py
 ┃ ┃ ┃ ┣ 📜middlewares.py
 ┃ ┃ ┃ ┣ 📜pipelines.py
 ┃ ┃ ┃ ┗ 📜settings.py
 ┃ ┃ ┗ 📜scrapy.cfg
 ┃ ┗ 📜chromedriver
 
 ```

## Data Sources: 

All data in this corpus was collected on Reddit from March 2, 2021 through December 31, 2021. All posts were scraped from the following subreddits during this collection window:

- worldnews
- news
- worldpolitics
- worldevents
- politics
- uspolitics
- AmericanPolitics
- AmericanGovernment
- Libertarian
- socialism
- progressive
- Conservative 
- democrats
- Liberal
- Republican
- LibertarianLeft


## Data Collection Methods: 
Data was scraped with PushShift API. Web crawling was performed using Scrapy-Splash with a  Docker integration. All posts in the data set were initially scraped for keywords that would initiate the presence of a visualization: [`chart`, `charts`, `interactive`, `interactives`, `viz`, `visualization`, `visualizations`, `graph`, `graphs`]. We examined both the DOM of the Reddit webpages in addition to the body text and title scraped from the post. 

To get images of the visualizations, we used the screenshot feature of Scrapy-Splash and did a manual check to ensure that the image contained a visualization.

## Data Organization: 
There are two central folders where this data is available. All posts are found by month in the folder called “Reddit.” Posts that were found with visualizations are compiled in the spreadsheet called [cleaned_data](https://docs.google.com/spreadsheets/d/11ULjFTGqqZJw8iJbgyEKGL9ahp3sosLA4E4jG7cZgUs/edit?usp=sharing). The following columns are listed in all spreadsheets:

- Date: The date the post was scraped using Scrapy-Splash. 
- Subreddit: The subreddit where the post lives. 
- Title: The title of the Reddit post by the user. 
- Post URL: Any URLs the user  in the post text
- ID: The unique ID that is automatically assigned to the Reddit post.
- Chart Type: The type of chart identified in the post. 
- Score: Describes the difference in “upvotes” and “downvotes” from users. 
- Total Comments: The total number of comments the post received as of the collection date. 	
- Score + Comments: The sum of the number of comments and the score of the post. 
- Colorized_Entropy: The amount of information (measured in bits) that the visualization has as determined by Shannon’s Entropy. 
This was used to proxy visual complexity for the purposes of this thesis. 															
