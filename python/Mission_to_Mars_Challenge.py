#!/usr/bin/env python
# coding: utf-8

# In[219]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[220]:


# Windows users
executable_path = {'executable_path': 'C:/Users/Gagandeep/chromedriver_win32/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[221]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[222]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[223]:


slide_elem.find("div", class_='content_title')


# In[224]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[225]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[226]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[227]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[228]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[229]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[230]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# In[231]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()


# In[232]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[233]:


df.to_html()


# In[256]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[257]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
hemisphere_image_urls = []
lists = browser.find_by_css('a.product-item img')

for item in range(len(lists)):
    hemisphere = {}
    
    browser.find_by_css('a.product-item img')[item].click()
    test_img = browser.find_by_text('Sample').first
    hemisphere['img_url'] = test_img['href']
    hemisphere['title'] = browser.find_by_css('h2.title').text
    #print(browser.find_by_css('h2.title').text)
    hemisphere_image_urls.append(hemisphere)
    browser.back()


# In[258]:


# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)


# In[259]:


# 5. Quit the browser
browser.quit()


# In[ ]:




