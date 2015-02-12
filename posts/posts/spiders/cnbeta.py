# -*- coding: utf-8 -*-
from hashlib import md5

import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import log

from items import CnbetaItem


class CnbetaSpider(CrawlSpider):
    def __init__(self, *a, **kw):


        super(CnbetaSpider, self).__init__(*a, **kw)


    name = "cnbeta"
    allowed_domains = ["cnbeta.com"]
    start_urls = (
        'http://m.cnbeta.com/list_latest_1.htm',
        # 'http://www.cnbeta.com/articles/367535.htm',
    )

    rules = (
        Rule(SgmlLinkExtractor(allow=('.*\/list_latest_.*\.htm', )),
             callback='parse', follow=True
        ),
        Rule(SgmlLinkExtractor(allow=('.*\/view_.*\.htm', )),
             callback='parse_articles', follow=True
        ),
    )

    # def start_requests(self):
    #     return [scrapy.FormRequest("http://www.example.com/login",
    #                            formdata={'user': 'john', 'pass': 'secret'},
    #                            callback=self.logged_in)]

    def save_html(self, response):
        self.log('[start] save_html:' + response.url, level=log.DEBUG)

        filename = 'html/' + md5(response.url).hexdigest() + '.html'
        open(filename, 'wb').write(response.body)
        self.log('[finish] save_html:' + response.url, level=log.DEBUG)


    def parse(self, response):
        self.save_html(response)

        sel = Selector(response)

        all_url_list = sel.xpath('//a')

        for url_item in all_url_list:
            link = url_item.xpath('@href').extract()
            if len(link) > 0:
                next_url = ''

                if link[0].startswith('http://m.cnbeta.com/'):
                    next_url = link[0]
                elif link[0].startswith('/'):
                    next_url = 'http://m.cnbeta.com' + link[0]

                if next_url != '':

                    if next_url.startswith('http://m.cnbeta.com/view_'):
                        self.log('start parse articles :' + next_url, level=log.INFO)
                        yield scrapy.Request(url=next_url, callback=self.parse_articles)

                    elif next_url.startswith('http://m.cnbeta.com/list_latest_'):
                        self.log('start parse list :' + next_url, level=log.INFO)
                        yield scrapy.Request(url=next_url, callback=self.parse)

                    else:
                        self.log('url has no rule to match :' + next_url)

                else:
                    self.log('url has no rule to match :' + next_url)

                    #return item


    def parse_articles(self, response):
        self.save_html(response)

        item = CnbetaItem()
        sel = Selector(response)

        #item['title'] = sel.xpath('//title/text()').extract()
        item['url'] = response.url
        item['title'] = sel.xpath("//h1[@class='article-tit']/text()").extract()
        item['introduction'] = sel.xpath("//div[@class='article-summ']/text()").extract()
        item['content'] = sel.xpath("//div[@class='articleCont']").extract()
        item['post_time'] = sel.xpath("//time[@class='time']/text()").extract()

        return item


    def add_cookie(self, request):
        self.log("add_cookie now", level=log.INFO)
        request.replace(cookies=[
            {'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': 'DOMAIN', 'path': '/'},
        ])
        return request
