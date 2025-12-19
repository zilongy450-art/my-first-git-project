# api/toggle_video_api.py
class ToggleVideoAPI:
    def __init__(self, client):
        self.client = client

    def toggle(self, *, hash_: str, video_id: str, list_id: str, ts: int):
        path = "/aj/lists"
        params = {
            "hash": "d003833f9f38f2c93f587610988cbbb761e0e3bd",
            "type": "list",
            "a": "tg",
            "id": "91",
            "list": str(list_id),

        }
        resp = self.client.request("GET", path, params=params)
        return resp
