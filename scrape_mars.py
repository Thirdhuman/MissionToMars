
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import pymongo
import time
import pandas as pd
import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#get_ipython().system('which chromedriver')
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    mars_db = {}
    output = marsNews()
    mars_db["mars_news"] = title
    mars_db["mars_paragraph"] = body
    mars_db["mars_image"] = marsImage()
    mars_db["mars_weather"] = marsWeather()
    mars_db["mars_facts"] = marsFacts()
    mars_db["mars_hemisphere"] = marsHem()

    return mars_db

def marsNews():
    url_nasa = 'https://mars.nasa.gov/news/'
    browser.visit(url_nasa)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #item_list = soup.find_all('ul', class_="item_list")
    title = soup.find('div', class_="content_title").text
    body = soup.find('div', class_="article_teaser_body").text

def marsImage():
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    #image
    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")
    image = soup.find('figure', class_='lede').a['href']
    feat_image_url= "https://www.jpl.nasa.gov/" + image

def marsWeather():
    url_mars="https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars)
    mars_html=browser.html
    soup=BeautifulSoup(mars_html, 'html.parser')
    mars=soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars)

def marsFacts():
    url_space="https://space-facts.com/mars/"
    browser.visit(url_space)
    html_space = browser.html
    soup = BeautifulSoup(html_space, 'html.parser')
    table_data =soup.find('table', class_="tablepress tablepress-id-mars")
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


    # Astrogeology Data
    url_astrogeology = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_astrogeology)
    html_astrogeology = browser.html
    soup = BeautifulSoup(html_astrogeology, "html.parser")
    returns = soup.find('div', class_="collapsible results")
    hemis = returns.find_all('div', class_="description")
    image_urls =[]
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
    # Create Database in the form of a dictionary

mars_db = {"id": 1,
                "news_title": title,
                "news_text": body,
                "featured_image_url": feat_image_url,
                "weather_mars": mars,
                "mars_table": space_html,
                "mars_hemisphere": image_urls}

    return mars_db
