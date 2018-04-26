# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    # Set the executable path and initialize the chrome browser in splinter
    browser = init_browser()

    # Create an empty Python dictionary to get all of the scraped data
    mars = {}


    
    ### NASA Mars News
    # Set the url for the mars.nasa website
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(2)

    # Create BeautifulSoup object and parse with 'html.parser'
    nasa_news_soup = BeautifulSoup(browser.html, 'html.parser')

    # Examine the results, then determine element that contains latest News Title
    results_news_title = nasa_news_soup.find('div', class_='content_title')

    # Find the first <a> tag and save it as `first_news_title`
    news_title = results_news_title.find('a').get_text()
    mars["news_title"] = news_title

    # Examine the results, then determine element that contains the paragraph
    results_news_paragraph = nasa_news_soup.find('div', class_='article_teaser_body')

    # Find the paragraph text using the parent element
    news_p = results_news_paragraph.text
    mars["news_p"] = news_p



    ### JPL Mars Space Images

    # Set the url for the jpl.nasa website
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(2)

    # Examine the results, then determine element that contains full image
    jpl_full_image = browser.find_by_id('full_image')

    # Click the 'full image' button(link)
    time.sleep(2)
    jpl_full_image.click()
    time.sleep(2)

    # Examine the results
    # This page has a medium-size image. Determine element that contains more info since more ifo link has a large size image.
    jpl_more_info = browser.find_link_by_partial_text('more info')

    # Click the 'more info' button(link)
    jpl_more_info.click()
    time.sleep(2)

    # This page has the full image. grab the html from this page.
    # Create BeautifulSoup object and parse with 'html.parser'
    jpl_image_soup = BeautifulSoup(browser.html, 'html.parser')

    # Find the image url for the current Featured Mars Image
    mars_image_url = jpl_image_soup.find('figure', class_='lede').find('img')['src']
    #print(mars_image_url)

    # Assign the url string to a variable called `featured_image_url` and get a complete url
    featured_image_url = "https://www.jpl.nasa.gov" + mars_image_url
    mars["featured_image_url"] = featured_image_url



    ### Mars Weather

    # Set the url for the mars weather website
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(2)

    # Create BeautifulSoup object and parse with 'html.parser'
    mars_weather_soup = BeautifulSoup(browser.html, 'html.parser')

    # Examine the results, then determine element the latest tweet text
    mars_weather = mars_weather_soup.find('p', class_='tweet-text').text
    mars["mars_weather"] = mars_weather



    ### Mars Facts

    # Read the html for the table
    mars_facts_df = pd.read_html('http://space-facts.com/mars/')[0]

    # Rename the column headers
    mars_facts_df.columns = ['Description', 'Value']

    # Set the index to Column 1
    mars_facts_df.set_index('Description', inplace=True)

    # Use Pandas to convert the data to a HTML table string.
    mars_facts = mars_facts_df.to_html()
    mars_facts = mars_facts.replace('\n', '')
    mars["mars_facts"] = mars_facts
    


    ### Mars Hemispheres

    # Set the url for the mars hemisplere images website
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    time.sleep(2)

    # Create BeautifulSoup object and parse with 'html.parser'
    mars_hemispheres_soup = BeautifulSoup(browser.html, 'html.parser')

    # Examine the results, then determine element that contains first full image
    # 'dive'with class result-list contains 4 'div' with class item
    products = mars_hemispheres_soup.find('div', class_='result-list')
    mars_hemispheres = products.find_all('div', class_='item')

    # Creater a dictionary to hold the values for image url and titles
    mars_hemisphere_dict = []

    # iterate through the element to get the image url and titles
    for item in mars_hemispheres:
        
        title = item.find("h3").text
        
        just_image_url = item.find('a')['href']
        complete_image_url = "https://astrogeology.usgs.gov/" + just_image_url    
        browser.visit(complete_image_url)
        time.sleep(2)
        
        item_soup=BeautifulSoup(browser.html, 'html.parser')
        
        downloads = item_soup.find('div', class_='downloads')
        image_url = downloads.find('a')['href']
        
        mars_hemisphere_dict.append({"title": title, "img_url": image_url})

    mars["mars_hemisphere_dict"] = mars_hemisphere_dict

    browser.quit()

    return mars


