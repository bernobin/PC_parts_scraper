import requests

URL = "https://www.toppreise.ch"

headers = {
        'authority': 'www.toppreise.ch',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'de-DE,de;q=0.9',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }


class Requester:
    def __init__(self):
        self.session = requests.Session()

    def get_front_page(self):
        print('requesting:', URL)
        return self.session.get(URL, headers=headers)

    def get_products_list(self, endpoint, filters=''):
        print('requesting:', URL + endpoint + filters)
        return self.session.get(URL + endpoint + filters, headers=headers)