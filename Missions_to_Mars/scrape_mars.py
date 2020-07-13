def scrape():

    # Import dependencies
    from bs4 import BeautifulSoup
    import requests
    from splinter import Browser
    import pandas as pd
    import time
    import re
    
    returnD = {}

    # Executable path
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', executable_path)

    # NASA News

    # Grab url
    nasa_url = "https://mars.nasa.gov/news/"

    browser.visit(nasa_url)
    time.sleep(5)

    # Define html variable to browser and initiate BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Search for news titles
    title_results = soup.find_all('div', class_='content_title')

    # Search for paragraph text under news titles
    p_results = soup.find_all('div', class_='article_teaser_body')

    # Extract first title and paragraph, and assign to variables
    news_title = title_results[0].text
    news_p = p_results[0].text
    
    returnD['news_title'] = news_title
    returnD['news_p'] = news_p

    # JPL Mars Space Images - Featured Image

    # Grab url
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Visit browser
    browser.visit(featured_image_url)

    # Define image variable to html
    image = browser.html

    # Initiate Beautiful Soup
    soup = BeautifulSoup(image, 'html.parser')

    image_results = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_page = 'https://www.jpl.nasa.gov'

    image_results = main_page + image_results
    returnD['featured_image_url'] = image_results

    # Mars Weather

    # Grab URL and visit browser
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html = browser.html

    # Beautiful Soup
    weather_soup = BeautifulSoup(html, 'html.parser')

    # Scrape Mars Weather tweet using 'try' and 'except'
    mars_weather = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    try:
        weather = mars_weather.find("p", "tweet-text").get_text()
        weather
    except AttributeError:
        pattern = re.compile(r'sol')
        weather = weather_soup.find('span', text = pattern).text
        weather
    returnD['mars_weather'] = weather

    # Mars Facts

    # Print Mars Facts into a DataFrame
    mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]

    # Create DataFrame to_html
    mars_facts_table = [mars_facts_df.to_html(classes='data table table-borderless', index=False, header=False, border=0)]
    returnD['mars_facts_table'] = mars_facts_table

    # Mars Hemispheres

    # Grab url and visit browser
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    # Find elements on each loop 
    image_urls_hemispheres = []

    links = browser.find_by_css("a.product-item h3")

    # For i in range (loop)
    for i in range(len(links)):
        browser.find_by_css("a.product-item h3")[i].click()
        hemisphere = {}
        
    # Find sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        
    # Get hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        
    # Append hemisphere object to list
        image_urls_hemispheres.append(hemisphere)
        
    # Navigate backwards
        browser.back()
        
    # Find elements on each loop 
    image_urls_hemispheres = []

    links = browser.find_by_css("a.product-item h3")

    # For i in range (loop)
    for i in range(len(links)):
        browser.find_by_css("a.product-item h3")[i].click()
        hemisphere = {}
        
    # Find sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        
    # Get hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        
    # Append hemisphere object to list
        image_urls_hemispheres.append(hemisphere)
        
    # Navigate backwards
        browser.back()
    
    returnD['hemisphere_image_urls'] = image_urls_hemispheres
    return returnD




