import time
import pathlib
import yaml
import pytest

from core.http_client import HttpClient
from api.create_list_api import CreateListAPI

from config import BASE_URL, HASH, COOKIE, UA

DATA_FILE = pathlib.Path(__file__).parent.parent / "data" / "create_list.yaml"


def load_cases():
    return yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))


def render_name(s: str) -> str:
    return s.replace("${ts}", str(int(time.time())))


@pytest.fixture(scope="session")
def api():
    client = HttpClient(base_url=BASE_URL, cookie=COOKIE, user_agent=UA)
    return CreateListAPI(client)


@pytest.mark.parametrize("case", load_cases(), ids=lambda c: f'{c["id"]}-{c["title"]}')
def test_create_list(api, case):
    name = render_name(case["name"])
    pr = case.get("pr", 1)

    resp = api.create(hash_=HASH, name=name, pr=pr)

    assert resp.status_code == case["expect_http"]
    j = resp.json()
    assert j.get("status") == case["expect_status"]
