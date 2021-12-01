import scrapy

class nbcnewsspider(scrapy.Spider):
    name = 'nbcnews'
    start_urls = ['https://www.nbcnews.com/western-wildfires']

    def parse(self, response):
        for articles in response.css('div.wide-tease-item__wrapper'):
            yield {
                'title': articles.css('h2.wide-tease-item__headline::text').get(),
                'link': articles.css('a').attrib['href'],
                'date': articles.css('div.wide-tease-item__timestamp::text').get()
            }