from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem

import json

class ArticlesExtractor(BasePortiaSpider):
    name = "articles_extractor"
    allowed_domains = [u'link.springer.com']
    with open('links.json') as file:
        json_data = json.load(file)
        links = []
        for item in json_data:
            links.append(item['link'][0])

    start_urls = links
    # start_urls = [u'https://link.springer.com/article/10.1007/s10606-017-9279-8']
    rules = [
        Rule(
            LinkExtractor(
                allow=('.*'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [[Item(PortiaItem,
                   None,
                   u'.FulltextWrapper',
                   [Field(u'title',
                          '.ArticleHeader > .MainTitleSection > .ArticleTitle *::text',
                          []),
                       Field(u'abstract',
                             '.Abstract > .Para *::text',
                             [])])]]
