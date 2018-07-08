import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://wahu.tv/player/56467-1-24.html/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        print("filename",filename)
        with open(filename, 'wb') as f:
            f.write(response.body)