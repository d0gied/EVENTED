import datetime
import pickle
from dataclasses import dataclass
from datetime import datetime

from common_utils.celery import get_app
from common_utils.codenrock import ICodenrock
from common_utils.database import IDatabase
from common_utils.models.event import Event, EventDict
from fake_useragent import UserAgent
from requests import Session

LINK = "https://codenrock.com"


def fetch_contests(page: int = 1) -> dict:
    ua = UserAgent().random
    session = Session()
    res = session.get(LINK, headers={"User-Agent": ua})
    cookies = res.cookies
    headers = {
        "user-agent": ua,
        "x-requested-with": "XMLHttpRequest",
        "x-csrf-token": cookies.get("XSRF-TOKEN"),
        "x-xsrf-token": cookies.get("XSRF-TOKEN"),
    }
    res = session.get(
        f"{LINK}/contests?page={page}",
        headers=headers,
    )
    return res.json()


@dataclass
class Info:
    pages: int
    count: int


def get_info() -> Info:
    info = fetch_contests()
    return Info(pages=info["pagesCount"], count=info["countContests"])


def get_contests(page: int = -1):
    if page != -1:
        return fetch_contests(page)["contests"]
    info = get_info()
    contests = []
    for page in range(1, info.pages + 1):
        data = fetch_contests(page)
        contests.extend(data["contests"])
    return contests


def load_contests():
    import os

    if os.path.exists("contests.pkl"):
        with open("contests.pkl", "rb") as f:
            update_time, data = pickle.load(f)
            update_time: datetime
        if (datetime.now() - update_time).seconds < 60 * 10:
            print("Using cached data")
            return data
        print("Updating data")
    else:
        print("No cached data")

    data = get_contests()
    update_time = datetime.now()
    with open("contests.pkl", "wb") as f:
        pickle.dump((update_time, data), f)
    return data


app = get_app("codenrock")

app.conf.beat_schedule = {
    "parse": {
        "task": "codenrock.parse",
        "schedule": 60.0,
    }
}


class Codenrock(ICodenrock):
    @staticmethod
    @app.task(name="codenrock.get_events")
    def get_events() -> list[EventDict]:
        events = []
        for contest in load_contests():
            try:
                event = Event.model_validate(contest)
                events.append(event.model_dump())
            except Exception as e:
                print(e)
        return events

    @staticmethod
    @app.task(name="codenrock.parse")
    def parse() -> None:
        events = Codenrock.get_events()
        return app.send_task("add_events", args=[events])
