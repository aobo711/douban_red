# -*- coding: utf-8 -*-
from scrapy.http import Request,FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector
import urllib, sys, json, os

reload(sys)  
sys.setdefaultencoding('utf8')  

class DoubanSpider(Spider):
    name = 'douban'
    allowed_domains = []

    start_urls = [
        'https://douban.fm/j/v2/redheart/basic'
    ]
    
    def __init__(self):
        self.headers = {}
        self.cookies = {
            'bid' :'IMOdXj6L4Fk',
            'flag' : 'ok',
            'ac=' : 1463109427,
            '_gat' : 1,
            '_vwo_uuid_v2' : '43B27C8451B59518903C5E9AF456F06A|6d793456673628407946c198195bd31f',
            '_pk_id.100002.6447' : '606a9ae8f7ea76a2.1458314333.3.1463109434.1459432650.',
            '_pk_ses.100002.6447' : '*',
            'dbcl2' : '2204709:w6GEioD+wBw',
            'fmNlogin' : 'y',
            'ck' : '0zUj',
            '_ga' : 'GA1.2.891626739.1458314332'
        }

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                          headers = self.headers, \
                          cookies = self.cookies,
                          callback = self.parse)


    def parse_detail(self, response):
        songs = json.loads(response.body_as_unicode())
        songs = songs[21:]
        for s in songs:
            title = s['title']
            artist = s['artist']
            file_ext = s['file_ext']
            
            target = '"/Users/jintian/Music/douban/' + title + '-' + artist + '.' + file_ext + '"'

            cmd = 'curl -o %s %s' % (target, s['url'])

            os.system(cmd)

    def parse(self, response):
        basic = json.loads(response.body_as_unicode())
        songs = basic['songs']
        sids = [s['sid'] for s in songs]

        songs_api = 'https://douban.fm/j/v2/redheart/songs'

        formdata = {
            'sids' : '|'.join(sids),
            'kbps' : '192',
            'ck' : '0zUj'
        }
        
        request = FormRequest(songs_api, 
            cookies = self.cookies,
            formdata = formdata,
            callback=self.parse_detail)

        yield request

