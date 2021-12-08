import scrapy
from selenium import webdriver

class nbcnewsspider(scrapy.Spider):
    name = 'nbcnews'
    start_urls = ['https://www.nbcnews.com/western-wildfires']

    def parse(self, response):
        driver = webdriver.Firefox()
        driver.get(self.start_urls[0])
        element = driver.find_elements_by_class_name("feeds__load-more-button")
        element.click
        html = element.page_source

        for articles in html.css('div.wide-tease-item__wrapper'):
            yield {
                'title': articles.css('h2.wide-tease-item__headline::text').get(),
                'link': articles.css('a').attrib['href'],
                'date': articles.css('div.wide-tease-item__timestamp::text').get()
            }
        
        driver.quit()