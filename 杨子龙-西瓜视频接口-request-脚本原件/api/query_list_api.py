# api/query_list_api.py
class QueryListAPI:
    def __init__(self, client):
        self.client = client

    def query(self, *, hash_: str, video_id: str, ts: int):
        path = "/aj/lists"
        params = {
            "hash": "d003833f9f38f2c93f587610988cbbb761e0e3bd",
            "type": "list",
            "a": "add",
            "id": "91",

        }
        resp = self.client.request("GET", path, params=params)
        return resp
