import time
import pathlib
import yaml
import pytest

from core.http_client import HttpClient
from api.query_list_api import QueryListAPI

from config import BASE_URL, HASH, COOKIE, UA

DATA_FILE = pathlib.Path(__file__).parent.parent / "data" / "query_list.yaml"


def load_cases():
    return yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def api():
    client = HttpClient(base_url=BASE_URL, cookie=COOKIE, user_agent=UA)
    return QueryListAPI(client)


@pytest.mark.parametrize("case", load_cases(), ids=lambda c: f'{c["id"]}-{c["title"]}')
def test_query_list(api, case):
    resp = api.query(hash_=HASH, video_id=case["video_id"], ts=int(time.time() * 1000))

    assert resp.status_code == case["expect_http"]
    j = resp.json()
    assert j.get("status") == case["expect_status"]

    if case.get("expect_html_not_empty"):
        assert j.get("html"), "html为空：可能cookie失效/未登录/被风控"
