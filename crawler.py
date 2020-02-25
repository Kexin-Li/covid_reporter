import time
import requests

from parser import parse
from reporter import report


headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}


def get_url():
    # to be filled
    base_url = 'url'
    return base_url


def get_detail_url(id):
    base_url = 'https://m.weibo.cn/statuses/extend?id='
    return base_url + id


def crawl():
    f = requests.get(get_url(), headers)
    feed = f.json()
    cards = feed['data']['cards']
    
    for card_group in cards:
        if 'card_group' in card_group:
            for card in card_group['card_group']:
                if card['card_type'] == '9':
                    pics = []
                    id = card['mblog']['id']

                    if 'pics' in card['mblog']:
                        for pic in card['mblog']['pics']:
                            pics.append(pic['large']['url'])

                    try:
                        d = requests.get(get_detail_url(id), headers)
                        detail = d.json()
                    except Exception:
                        continue

                    if detail:
                        text = detail['data']['longTextContent']

                        try:
                            info = parse(id, text, pics)
                        except Exception:
                            continue
                        if info:
                            res = report(info)


if __name__ == '__main__':
    while True:
        crawl()
        time.sleep(5)
