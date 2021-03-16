# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Windows users
executable_path = {'executable_path': 'C:/Users/Gagandeep/chromedriver_win32/chromedriver'}
browser = Browser ('chrome', **executable_path, headless=False)

def scrape_all():
    executable_path = {'executable_path': 'C:/Users/Gagandeep/chromedriver_win32/chromedriver'}
    browser = Browser ('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()

    dict = {
        "news_paragraph" : news_p,
        "news_title" : news_title,
        "featured-image" : img_url,
        "facts" : facts
    }
    return dict


def mars_news(browser):
# Visit the mars nasa news site
   url = 'https://mars.nasa.gov/news/'
   browser.visit(url)

   # Optional delay for loading the page
   browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

   # Convert the browser html to a soup object and then quit the browser
   html = browser.html
   news_soup = soup(html, 'html.parser')
   news_title =''
   news_paragraph = ''
   # Add try/except for error handling
   try:
       slide_elem = news_soup.select_one("ul.item_list li.slide")
       slide_elem.find("div", class_="content_title")

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
       news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
       news_paragraph = slide_elem.find("div", class_="article_teaser_body").get_text()

   except AttributeError:
       return 'Testing Proves Its Worth With Successful Mars Parachute Deployment', 'The giant canopy that helped land Perseverance on Mars was tested here on Earth at NASA’s Wallops Flight Facility in Virginia'
    
   return news_title, news_paragraph
   

def featured_image(browser):
# Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

# Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
# Add try/except for error handling
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

# Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()




