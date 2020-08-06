# Step 1 Import the necessary libraries (some of the libraries are provided below)
import pandas as pd
from string import punctuation, whitespace
from bs4 import BeautifulSoup
import numpy as np
import markdown
import re

# Step 2 Display the data scraped using Scrapy (Hint: use pandas)
data_main = pd.read_csv("CarTalkCommunityMain.csv")
data_posts = pd.read_csv("CarTalkCommunityPost.csv")
data_main.head()
data_posts.head()

# Step 3 Display all of the posts from the CSV file
data_main[['title']].head()
data_posts[['cooked']].head()

# Step 4 Convert the Text from the Post from Markdown formatting to HTML Formatted Text to Raw Text 
# (Hint: Take a look at the 'markdown' and 're' libraries)
def markdown_to_raw_text(markdown_text):
  if not (markdown_text is np.nan or markdown_text is None):
    html = markdown.markdown(markdown_text)
    return "".join(BeautifulSoup(html).findAll(text=True))

raw_text = data_posts['cooked'].apply(markdown_to_raw_text)
raw_text.to_frame().head()

# Step 5 Remove punctuation marks and whitespace characters from the posts
# (Hint: What is a whitespace character? Are there multiple types of whitespace characters?)
def remove_non_alphanum_chars(raw_text):
  if not (raw_text is np.nan or raw_text is None):
    return re.sub('[^A-Za-z0-9]+', ' ', raw_text).replace(" ", "")

alphanum_removed = raw_text.apply(remove_non_alphanum_chars)
alphanum_removed.to_frame().head()

# Step 6 Update the data scraped using Scrapy to contain the formatted posts
def process_post_text(post_df):
  temp = post_df.copy()
  temp['cooked'] = temp['cooked'].apply(markdown_to_raw_text).apply(remove_non_alphanum_chars)
  return temp

data_posts_processed = process_post_text(data_posts)
data_posts_processed.head()