import requests


headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/x-www-form-urlencoded",
}


def report(info):
    # to be filled
    url = "url"

    data = {
        "name": info["name"],
        "question": info["question"],
        "desc": info["desc"],
        "addr": info["addr"],
        "contact": info["contact"],
        "phone": int(info["phone"]),
        "province": info["province"],
        "city": info["city"],
        "region": info["region"],
    }

    if 'pics' in info:
        if len(info['pics']) > 2:
            data['img[2][url]'] = info['pics'][2]
            data['img[1][url]'] = info['pics'][1]
            data['img[0][url]'] = info['pics'][0]
        elif len(info['pics']) > 1:
            data['img[1][url]'] = info['pics'][1]
            data['img[0][url]'] = info['pics'][0]
        elif len(info['pics']) > 0:
            data['img[0][url]'] = info['pics'][0]
    
    try:
        res = requests.post(url, data, headers=headers)
        return res.status_code
    except Exception:
        return res.status_code
