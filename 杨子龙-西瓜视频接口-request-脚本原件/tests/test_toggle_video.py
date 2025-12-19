import time
import pathlib
import yaml
import pytest

from core.http_client import HttpClient
from core.extractors import extract_list_id_by_name
from api.create_list_api import CreateListAPI
from api.query_list_api import QueryListAPI
from api.toggle_video_api import ToggleVideoAPI

from config import BASE_URL, HASH, COOKIE, UA

DATA_FILE = pathlib.Path(__file__).parent.parent / "data" / "toggle_video.yaml"


def load_cases():
    return yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))


def now_ms() -> int:
    return int(time.time() * 1000)


@pytest.fixture(scope="session")
def client():
    return HttpClient(base_url=BASE_URL, cookie=COOKIE, user_agent=UA)


@pytest.fixture(scope="session")
def apis(client):
    return (
        CreateListAPI(client),
        QueryListAPI(client),
        ToggleVideoAPI(client),
    )


@pytest.mark.parametrize("case", load_cases(), ids=lambda c: f'{c["id"]}-{c["title"]}')
def test_toggle_chain(apis, case):
    create_api, query_api, toggle_api = apis
    video_id = case["video_id"]

    # 1) 创建一个新列表（避免重名）
    playlist_name = f"po链路_{int(time.time())}"
    r1 = create_api.create(hash_=HASH, name=playlist_name)
    assert r1.status_code == case["expect_http"]
    assert r1.json().get("status") == case["expect_status"]

    # 2) 查询拿 html
    r2 = query_api.query(hash_=HASH, video_id=video_id, ts=now_ms())
    assert r2.status_code == case["expect_http"]
    j2 = r2.json()
    assert j2.get("status") == case["expect_status"]
    html = j2.get("html", "")
    assert html

    # 3) 提取 list_id
    list_id = extract_list_id_by_name(html, playlist_name)
    assert list_id

    # 4) tg 两次翻转（添加/移除闭环）
    r3 = toggle_api.toggle(hash_=HASH, video_id=video_id, list_id=list_id, ts=now_ms())
    r4 = toggle_api.toggle(hash_=HASH, video_id=video_id, list_id=list_id, ts=now_ms())

    assert r3.status_code == case["expect_http"]
    assert r4.status_code == case["expect_http"]
    j3, j4 = r3.json(), r4.json()
    assert j3.get("status") == case["expect_status"]
    assert j4.get("status") == case["expect_status"]
    assert j3.get("code") in (0, 1)
    assert j4.get("code") in (0, 1)
    assert j3.get("code") != j4.get("code")
