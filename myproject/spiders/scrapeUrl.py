import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    allowed_domains = ['linkedin.com']
    start_urls = ['https://www.linkedin.com/school/indian-institute-of-management-bangalore/people/?educationEndYear=2023&educationStartYear=2017&keywords=mba']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        # Scroll till the end of the page
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Adjust time according to your needs
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Now, scrape the loaded page
        sel = Selector(text=self.driver.page_source)
        profiles = sel.css('div.org-people-profile-card__profile-info')

        for profile in profiles:
            name = profile.css('div.lt-line-clamp--single-line::text').get()
            profile_url = profile.css('a.link-without-visited-state::attr(href)').get()

            yield {
                'Name': name,
                'Profile URL': response.urljoin(profile_url)
            }

        self.driver.quit()

# To run this spider, save it in a file and run it using Scrapy command line tools
