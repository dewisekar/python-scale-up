from re             import findall, compile
from time           import time, sleep
from json           import loads
from requests       import Session, get, head, post
from hashlib        import sha256
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
import requests
from lxml import etree
from io import StringIO
import json
from datetime import datetime

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
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        print("5")
        #proxies = livecounts.__getProxies()
        #print(proxies)
        #req = get(f'https://tiktok.livecounts.io/video/stats/{video_id}', headers=headers, proxies=proxies)
        req = get(f'https://tiktok.livecounts.io/video/stats/{video_id}', headers=headers)
        print("6", req)
        return req.json()

    @staticmethod
    def user_search(username: (int or str)) -> dict:
        timestamp = int(time() * 1000)
        
        headers = {
            # **livecounts.__signature(timestamp),
            'authority' : 'tiktok.livecounts.io',
            'origin'    : 'https://livecounts.io',
            'host'      : 'tiktok.livecounts.io',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        # proxies = livecounts.__getProxies()
        #print(proxies)
        #req = get(f'https://tiktok.livecounts.io/video/stats/{video_id}', headers=headers, proxies=proxies)
        #print("username:",username)
        req = get(f'https://tiktok.livecounts.io/user/search/{username}', headers=headers)
        print("req.json():",req.json())
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
            'authority' : 'tiktok.livecounts.io',
            'origin'    : 'https://livecounts.io',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        # proxies = livecounts.__getProxies()
        # print(proxies)
        req = get(url, headers=headers, allow_redirects=False)
        print("status",req.status_code)  # 302
        print("url header", req.headers['Location'])

        return req.headers['Location']


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

def getListVideoFromTiktokUser(username):
    listVideo = []
    if username[0:1] != '@':
        username = '@' + username
    try :
        parser = etree.HTMLParser()
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        page = requests.get(f'https://www.tiktok.com/{username}',headers=headers)
        html = page.content.decode("utf-8")
        tree = etree.parse(StringIO(html), parser=parser)
        refs = tree.xpath("//a")
        links = [link.get('href', '') for link in refs]
        listVideo = [l.split("/")[5] for l in links if '/video/' in l][:10]
    except Exception as e:
        print('got exception getListVideoFromTiktokUser, e:',e)
    return listVideo

def getVideoDataAndStats(videoId,username):
    resp = {}
    if username[0:1] != '@':
        username = '@' + username
    try:
        parser = etree.HTMLParser()
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        page = requests.get(f'https://www.tiktok.com/{username}/video/{videoId}',headers=headers)
        html = page.content.decode("utf-8")
        tree = etree.parse(StringIO(html), parser=parser)
        id_path = "SIGI_STATE"
        results = tree.xpath("//script[@id = '%s']" % id_path)
        videoData = json.loads(results[0].text)
        unixTimeStamps = videoData['ItemModule'][videoId]['createTime']
        ts = int(unixTimeStamps)
        createTime = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        data = {'cover:': videoData['ItemModule'][videoId]['video']['cover'],"title": videoData['SEOState']['metaParams']['title'],"createTime":createTime}
        stats = videoData['ItemModule'][videoId]['stats']
        resp = {'id':videoId,'data':data,'stats':stats}
    except Exception as e:
        print('got exception getCreatedTime, e:',e)
    return resp

if __name__ == '__main__':
    try:
        # print(livecounts.video_info(livecounts.link_to_id('https://www.tiktok.com/@anggianisl/video/7149484690917854491?_r=1&_t=8W8orM09DZR&is_from_webapp=v1&item_id=7149484690917854491')))
        #print(livecounts.video_info('7149484690917854491'))
        print(getListVideoFromTiktokUser('anggianisl'))
        # proxy = ''
        # while proxy == '':
        #     proxies = get_proxies()
        #     proxy_pool = cycle(proxies)
        #     for i in range(0,len(proxies)):
        #         proxy = next(proxy_pool)
        
        #print(proxies,proxy)
        
    except Exception as e:
        print('got exc, e:',e)