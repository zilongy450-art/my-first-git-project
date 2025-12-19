# core/http_client.py
import requests

class HttpClient:
    def __init__(self, base_url: str, cookie: str, user_agent: str):
        self.base_url = base_url.rstrip("/")
        self.s = requests.Session()
        self.s.headers.update({
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": user_agent,
            "Referer": "http://www.ixigua.net/",  # 你也可以换成抓包里的那个
            "Origin": "http://www.ixigua.net",
            "Cookie": "SITE_TOTAL_ID=fd6b14f36abb36a67f6f46a3c4abafd7; cookieconsent_status=dismiss; PHPSESSID=sqr9mmvquakk4u9v2ovddjjjcj; Hm_lvt_777b72b6411a140ccea21069556babac=1764034490,1764308798,1764558449,1764756516; HMACCOUNT=57B056F1CFF19C07; mode=night; user_id=637aa8b048c874306f3f3f355d972cfc0e1472fa17652512392370fb77727b84de25f53dc251c66ec4; views=a%3A1%3A%7Bi%3A0%3Ba%3A2%3A%7Bi%3A0%3Bi%3A91%3Bi%3A1%3Bs%3A40%3A%26quot%3B3397aab8e388b849b7534fcbb0733667abb1ca7d%26quot%3B%3B%7D%7D; r=c3RyaW5n; auto=; _uads=a%3A2%3A%7Bs%3A4%3A%26quot%3Bdate%26quot%3B%3Bi%3A1766114435%3Bs%3A5%3A%26quot%3Buaid_%26quot%3B%3Ba%3A0%3A%7B%7D%7D; next_up_videos=%5B%2291%22%5D; last_ads_seen=1766028698; Hm_lpvt_777b72b6411a140ccea21069556babac=1766044311",  # 直接把 curl -b 那串原样粘进来
        })

    def request(self, method: str, path: str, *, params=None, data=None, headers=None):
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        resp = self.s.request(method, url, params=params, data=data, headers=headers)
        return resp
