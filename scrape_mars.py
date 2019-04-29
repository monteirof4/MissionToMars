# Mission to Mars

# Dependencies

# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup

import time

import pandas as pd

def scrape():

    # --NASA Mars News--

    # Open browser with the Nasa news webpage 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Wait for the page to load
    time.sleep(2)

    # Scrape the webpage and collect the latest News Title and Paragraph Text
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').a.text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Close browser window
    browser.quit()

    #print(news_title)
    #print(news_p)

    # --JPL Mars Space Images - Featured Image--

    # Open browser with the JPL Mars Space Images webpage 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')

    # Wait for the page to load
    time.sleep(2)

    # Scrape the webpage and collect the full size Featured Mars Image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find(id='fancybox-lock').div.img['src']
    featured_image_url =  'https://www.jpl.nasa.gov/' + featured_image_url

    # Close browser window
    browser.quit()

    #print(featured_image_url)

    # --Mars Weather--

    # Open browser with the Mars Weather twitter account webpage 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Wait for the page to load
    time.sleep(2)

    # Scrape the webpage and collect latest Mars weather tweet from the page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather_p = soup.find('p',class_='tweet-text').text
    mars_weather_a = soup.find('p',class_='tweet-text').a.text
    mars_weather = mars_weather_p.replace(mars_weather_a, '')

    # Close browser window
    browser.quit()

    #print(mars_weather)

    # --Mars Facts--

    # Scrape the webpage and collect lthe table containing facts about the planet
    url = 'https://space-facts.com/mars/'

    # Read webpage tables with pandas
    facts = pd.read_html(url)

    # Store facts table in a Dataframe
    df_facts = facts[0]
    df_facts.columns = ['description', 'value']
    df_facts.set_index('description', inplace = True)

    # Convert to HTML
    facts = df_facts.to_html()
    
    print(facts)

    # --Mars Hemispheres--

    # Open browser with the USGS Astrogeology webpage 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Scrape the webpage and collect high resolution images for each of Mar's hemispheres
    hemisphere_image_urls = []
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find(id="product-section").find_all('h3')

    for link in links:
        browser.click_link_by_partial_text(link.text)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        # Wait for the page to load
        time.sleep(2)
        
        # Scrape the image link
        post = {
                'title' : link.text,
                'img_url': soup.find(id="wide-image").find('a')['href']
        }
        
        hemisphere_image_urls.append(post)
        
        browser.click_link_by_partial_text('Back')
        
    # Close browser window
    browser.quit()

    #print(hemisphere_image_urls)

    mars_data = {}

    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p
    mars_data['featured_image_url'] = featured_image_url
    mars_data['mars_weather'] = mars_weather
    mars_data['facts'] = facts
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data