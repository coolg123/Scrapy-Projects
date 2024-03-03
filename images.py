import scrapy
import json
from scrapy.http import Request
import re
import random

def create_image_url(data):
    base_url = data["media"]["baseUri"]
    pretty_name = data["media"]["prettyName"]
    tokens = data["media"]["token"]
    full_view = data["media"]["types"][-3]
    height = full_view["h"]
    width = full_view["w"]
    _150 = data["media"]["types"][0]['c']

    _150 = re.sub(r'w_\d+', f'w_{width}', _150)
    _150 = re.sub(r'h_\d+', f'h_{height}', _150)
    token = random.choice(tokens)
    image_url = base_url + _150.replace('<prettyName>', pretty_name) + "?token=" + token

    return image_url

header = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.deviantart.com/the-hypnoman/gallery",
        "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": "\"Android\"",
        "Sec-Ch-Viewport-Height": "1277",
        "Sec-Ch-Viewport-Width": "1469",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
    }


class ImagesSpider(scrapy.Spider):
    name = "images"
    allowed_domains = ["deviantart.com"]

    def __init__(self, start_url=None, *args, **kwargs):
        super(ImagesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []

    def start_requests(self):
        
        cookies = {
                "_pxvid": "9948a61b-4c6b-11ee-a51f-ac1607864526",
                "auth_secure": "__b90f3ac403a6c8b3b1af%3B%22f4c67a62c519c41cc31dca98a69ad540%22",
                "userinfo": "__3720804864ae778bbcfb%3B%7B%22username%22%3A%22randomcoolgenius%22%2C%22uniqueid%22%3A%22bdafe0d623e4caeb3337648c9f6486e4%22%2C%22dvs9-1%22%3A1%2C%22ab%22%3A%22tao-hcs-1-a-3%7Ctao-12c-1-b-2%7Ctao-ot1-1-a-1%7Ctao-cou-1-b-4%22%2C%22pv%22%3A%22c%3D1%2C1%2C1%2C1%22%7D",
                "auth": "__79c70251c0d45e6c5f14%3B%22c5dad1c800c965dd0c54fe9f37d279dd%22",
                "td": "0:1349%3B3:445%3B6:610x275%3B10:445%3B12:1469.5384521484375x1277.5384521484375"
            }


        yield Request(self.start_urls[0], headers=header, cookies=cookies, callback=self.parse)

    def parse(self, response):
        response = json.loads(response.body)

        for image in response['results']:
            try:
                image_url = create_image_url(image)
                yield {
                    'image_name': image['media']["prettyName"],
                    'image_url': image_url,
                }
            except Exception as e:
                print(e)
                continue

        next_offset = response["nextOffset"]
        
        if next_offset != None:
            next_url = re.sub(r'offset=\d+', f'offset={next_offset}', self.start_urls[0])
            yield Request(next_url, headers=header, callback=self.parse)

