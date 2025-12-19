# api/create_list_api.py
class CreateListAPI:
    def __init__(self, client):
        self.client = client

    def create(self, *, hash_: str, name: str, desc: str = "", pr: int = 1):
        path = "/aj/lists"
        params = {"type": "list", "a": "new"}
        data = {
            "hash": hash_,
            "name": name,
            "desc": desc,
            "pr": str(pr),
        }
        # curl 里是 x-www-form-urlencoded，这里 requests 会自动按表单发
        resp = self.client.request("POST", path, params=params, data=data)
        return resp
