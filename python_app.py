
# coding: utf-8

# In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.
# 
# ## Step 1 - Scraping
# 
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# 
# Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.
# NASA Mars News
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.
# 
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
# 
# JPL Mars Space Images - Featured Image
# 
# Visit the url for JPL's Featured Space Image here.
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# Make sure to find the image url to the full size .jpg image.
# Make sure to save a complete url string for this image.
# 
# # Example:
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
# 
# Mars Weather
# 
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
# 
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
# 
# Mars Facts
# 
# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.
# 
# Mars Hemisperes
# 
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# 
# # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]

# In[1]:


from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import pprint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# In[2]:


get_ipython().system('which chromedriver')


# In[3]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


url_nasa = 'https://mars.nasa.gov/news/'
browser.visit(url_nasa)


# In[5]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')
#item_list = soup.find_all('ul', class_="item_list")
title = soup.find('div', class_="content_title").text
body = soup.find('div', class_="article_teaser_body").text
print(title +": \n" + "\n" + body)


# In[6]:


url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url_jpl)

browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(5)
browser.click_link_by_partial_text('more info')

#image
image_html = browser.html
soup = BeautifulSoup(image_html, "html.parser")
image = soup.find('figure', class_='lede').a['href']
feat_image_url = "https://www.jpl.nasa.gov/" + image


# In[7]:


print('x'*80)
print(image)
print('x'*80)
print(feat_image_url)
print('x'*80)


# In[8]:


url_mars="https://twitter.com/marswxreport?lang=en"
browser.visit(url_mars)


# In[9]:


mars_html=browser.html
soup=BeautifulSoup(mars_html, 'html.parser')
mars=soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars)


# In[10]:


url_space="https://space-facts.com/mars/"
browser.visit(url_space)
html_space = browser.html
soup = BeautifulSoup(html_space, 'html.parser')
table_data =soup.find('table', class_="tablepress tablepress-id-mars")

#pprint(table_data)


# In[11]:


# gen lists + loop thru elements
value_list = []
label_list =[]
table= table_data.find_all('tr')
for element in table:
    elements = element.find_all('td')
    value_list.append(elements[1].text)
    label_list.append(elements[0].text)
#Generate space output
space_df =pd.DataFrame({"label":label_list,"value":value_list})
space_html = space_df.to_html(header =False,index = False)
print(' < DF > ')
print('x'*70)
print('x'*70)
print(space_df)
print('x'*70)
print('x'*70)
print(' < HTML > ')
print('x'*70)
print('x'*70)
print(space_html)
print('x'*70)
print('x'*70)


# In[19]:


# Astrogeology Data
url_astrogeology = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_astrogeology)
html_astrogeology = browser.html
soup = BeautifulSoup(html_astrogeology, "html.parser")
returns = soup.find('div', class_="collapsible results")
hemis = returns.find_all('div', class_="description")
image_urls =[]


# In[18]:


#print(returns)
#print(hemispheres)


# In[21]:


#Hemisphere info
for item in hemis:
    title = item.h3
    link = "https://astrogeology.usgs.gov" + item.a['href']
    browser.visit(link)
    page = browser.html
    results = BeautifulSoup(page, 'html.parser')
    image_url = results.find('div', class_='downloads').find('li').a['href']
    image_dict = {}
    image_dict['title'] = title
    image_dict['img_url'] = image_url
    image_urls.append(image_dict)
    
print(image_urls)


# In[23]:


# Create Database in the form of a dictionary
mars_db = {"id": 1,
            "news_title": title,
            "news_text": body,
            "featured_image_url": feat_image_url,
            "weather_mars": mars,
            "mars_table": space_html,
            "mars_hemisphere": image_urls}

