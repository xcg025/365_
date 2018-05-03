import scrapy

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = []

    def start_requests(self):
        url_head = 'https://movie.douban.com/subject_search?search_text='
        with open('movie_name.txt', 'r') as f:
            for line in f.readlines():
                self.start_urls.append(url_head+line)

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        print(response.body.decode())