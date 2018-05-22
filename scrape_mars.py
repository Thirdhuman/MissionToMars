
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import config
import pandas as pd
import pprint
import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#get_ipython().system('which chromedriver')
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    mars_db = {}
    title_body = News()
    mars_db["mars_news"] = title_body[0]
    mars_db["mars_paragraph"] = title_body[1]
    mars_db["mars_image"] = Image()
    mars_db["mars_weather"] = Weather()
    mars_db["mars_facts"] = Facts()
    mars_db["mars_hemisphere"] = Hemisphere()
    return mars_db


# In[14]:
def News():
    url_nasa = 'https://mars.nasa.gov/news/'
    browser.visit(url_nasa)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find("div", class_='list_text')
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text
    title_body = [news_title, news_p]
    return title_body


# In[15]:
def Image():
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #image
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url



def Weather():
    import tweepy
    # Twitter API Keys
    from config import (consumer_key, 
                        consumer_secret, 
                        access_token, 
                        access_token_secret)

    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())        

    target_user = "MarsWxReport"
    tweet = api.user_timeline(target_user, count =1)
    mars_weather = ((tweet)[0]['text'])
    return(mars_weather)


# In[18]:

def Facts():
    url_facts="https://space-facts.com/mars/"
    browser.visit(url_facts)
    html_space = browser.html
    mars_data = pd.read_html(url_facts)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    # print(' < DF > ')
    # print('x'*70)
    # print(mars_data)
    # print('x'*70)
    # print(' < HTML > ')
    # print('x'*70)
    # print(mars_facts)
    # print('x'*70)
    return mars_facts

def Hemisphere():
    # Astrogeology Data
    url_astrogeology = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_astrogeology)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere


