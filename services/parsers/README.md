# Parsers

## Overview

Parsers are used to extract events from different sources and send them to the message broker.

## Features

- **Event Parsing**: Parse events and send them to the message broker.

## Tech Stack

- **Selenuim**: For web scraping.
- **BeautifulSoup**: For parsing HTML and XML documents.
- **Requests**: For sending HTTP requests.

## Development

Creation of new parsers is easy. Just create a new folder in the `parsers` directory and add [the necessary files](docs/monorepo-specs.md).

To make it work you need to create Celery worker, specify the schedule and run the worker.

Sample:

```python
app = get_app("codenrock")

app.conf.beat_schedule = {
    "parse": {
        "task": "codenrock.parse",
        "schedule": 60.0 * 10.0,
    }
}


class Codenrock(ICodenrock):
    @staticmethod
    @app.task(name="codenrock.get_events", queue="codenrock")
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
    @app.task(name="codenrock.parse", queue="codenrock")
    def parse() -> None:
        events = Codenrock.get_events()
        return app.send_task("add_events", args=[events], queue="database")
```