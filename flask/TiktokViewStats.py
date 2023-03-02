from re             import findall, compile
from time           import time, sleep
from json           import loads
from requests       import Session, get, head, post
from hashlib        import sha256
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback

class livecounts:
    @staticmethod
    def __getProxies() -> dict:
        proxy = ''
        while proxy == '':
            proxies = get_proxies()
            proxy_pool = cycle(proxies)
            for i in range(0,len(proxies)):
                proxy = next(proxy_pool)
        return {"http": proxy, "https": proxy}

    @staticmethod
    def __signature(timestamp: int) -> dict:
        
        return {
            'x-aurora' : str(3 * timestamp),
            'x-joey'   : str(timestamp),
            'x-maven'  : sha256(f"0AVwElhWi1IfwcZKSNzq7E^84hFQ4ykenNAxeY7r@6ho1oTd6Ug*!WC&p$2aGY8MLHEkH0i8XCwnj3#JqI1NzCb91$gNzLYCbbG@NqvQMbcf8W9v3%s#uzjP@z*!e9a41JNWBqRIMJ*ULuav5k8z4kBj2^BCC%!3q@N0zZOS^TL#GzVz@9fhjg&^mSWi&oU5GMoCu9{timestamp}".encode()).hexdigest(),
            'x-mayhem' : "553246736447566b58312f7a4f72413653425342717a6e4231596f7a4d59686564764842324b396478544443756669734d56706f4346334633456366724b6732",
            'x-midas'  : sha256(str(timestamp + 64).encode()).hexdigest()
        }
    
    @staticmethod
    def video_info(video_id: (int or str)) -> dict:
        timestamp = int(time() * 1000)
        
        headers = {
            # **livecounts.__signature(timestamp),
            'authority' : 'tiktok.livecounts.io',
            'origin'    : 'https://livecounts.io',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        #proxies = livecounts.__getProxies()
        #print(proxies)
        #req = get(f'https://tiktok.livecounts.io/video/stats/{video_id}', headers=headers, proxies=proxies)
        req = get(f'https://tiktok.livecounts.io/video/stats/{video_id}', headers=headers)
        return req.json()

    @staticmethod
    def video_data(video_id: (int or str)) -> dict:
        timestamp = int(time() * 1000)
        
        headers = {
            # **livecounts.__signature(timestamp),
            'authority' : 'tiktok.livecounts.io',
            'origin'    : 'https://livecounts.io',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        # proxies = livecounts.__getProxies()
        # print(proxies)
        req = get(f'https://tiktok.livecounts.io/video/data/{video_id}', headers=headers)
        
        return req.json()
        
    @staticmethod
    def user_stats(user_id: (int or str)) -> dict:
        timestamp = int(time() * 1000)
        
        headers = {
            # **livecounts.__signature(timestamp),
            'authority' : 'tiktok.livecounts.io',
            'origin'    : 'https://livecounts.io',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        # proxies = livecounts.__getProxies()
        # print(proxies)
        req = get(f'https://tiktok.livecounts.io/user/stats/{user_id}', headers=headers)
        
        return req.json()
    
    @staticmethod
    def link_to_id(video_link: (int or str)) -> str:
        return str(
            findall(r"(\d{18,19})", video_link)[0] if len(findall(r"(\d{18,19})", video_link)) == 1
            else findall(r"(\d{18,19})", head(video_link, allow_redirects=True, timeout=5).url)[0]
        )
    
    @staticmethod
    def getIdFromLongUrl(url: str) -> dict:
        print("this is short url", url)       
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        # proxies = livecounts.__getProxies()
        # print(proxies)
        req = get(url, headers=headers)
        
        return req.url


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

if __name__ == '__main__':
    try:
        # print(livecounts.video_info(livecounts.link_to_id('https://www.tiktok.com/@anggianisl/video/7149484690917854491?_r=1&_t=8W8orM09DZR&is_from_webapp=v1&item_id=7149484690917854491')))
        print(livecounts.video_info('7149484690917854491'))
        # proxy = ''
        # while proxy == '':
        #     proxies = get_proxies()
        #     proxy_pool = cycle(proxies)
        #     for i in range(0,len(proxies)):
        #         proxy = next(proxy_pool)
        
        #print(proxies,proxy)
        
    except Exception as e:
        print('got exc, e:',e)