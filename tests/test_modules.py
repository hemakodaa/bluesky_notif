from src.bluesky_notif.parser import Request, FeedParser
import pytest


def test_failing():
    r = Request("clara.phase-connect.com")
    feed = r.feed_from_file("example_response.json")
    p = FeedParser()
    with pytest.raises(ValueError) as excinfo:
        for post in feed:
            p.author()
        print(excinfo.value)
