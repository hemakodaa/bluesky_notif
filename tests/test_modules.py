from src.bluesky_notif.parser import Request, FeedParser
import pytest


def test_failing():
    r = Request("clara.phase-connect.com")
    feed = r.feed_from_file("example_response.json")
    p = FeedParser()
    # currently this is a nightmare to test
    with pytest.raises(ValueError) as excinfo:
        for post in feed:
            # if FeedParser is not refactored
            # error checking must exist on ALL methods.
            
            # refactor so that the feed is returned from a single method
            # which is used by all the other methods to simplify
            # error checking
            p.author()
    print(excinfo.value)
