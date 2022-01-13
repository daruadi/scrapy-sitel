import scrapy

class SitelSpider(scrapy.Spider):
    name = "jobs"
    start_urls = [
        'https://jobs.sitel.com/go/Customer-Service-Jobs/7758100/',
    ]
    custom_settings = {
        'FEED_FORMAT': 'jl',
        'FEED_URI': 'jobs.jl'
    }

    def parse(self, response):
        for row in response.css('tr.data-row'):
            url = response.urljoin(row.css('.jobTitle-link ::attr(href)').get())
            yield scrapy.Request(url, callback=self.open_url)
        
        num_of_page = len(response.css('#job-table > div.pagination-bottom > div > div > ul > li')) - 2
        if num_of_page > 1:
            next_page = response.css('#job-table > div.pagination-bottom > div > div > ul > li.active ::text').get()
            next_page = int(next_page)
            if next_page < num_of_page:
                next_url = f"{self.start_urls[0]}{next_page*25}"
                print("nexturl", next_url)
                yield scrapy.Request(next_url, callback=self.parse)
    
    def open_url(self, response):
        yield {
            'url': response.request.url,
            'title': response.css('h1 span ::text').get().strip(),
            'location': response.css('span.jobGeoLocation ::text').get().strip(),
            'reqid': response.css('span.joblayouttoken-label + span ::text').get().strip(),
            'description': response.css('span.jobdescription div').get().strip(),
            'posteddate': response.css('div.jobDisplayShell > meta ::attr(content)').get()
        }