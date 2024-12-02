from src.bluesky_notif.parser import Request, FeedParser
import pytest


def test_failing_post_is_not_set():
    r = Request("clara.phase-connect.com")
    feed = r.feed_from_file("example_response.json")
    p = FeedParser()
    # p.post is not set
    with pytest.raises(ValueError) as excinfo:
        for post in feed:
            p.post_author()
        print(excinfo.value)
