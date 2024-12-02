from src.bluesky_notif.parser import Request, FeedParser


def test_request():
    Request("clara.phase-connect.com")


def test_parser_record_text_from_file():
    r = Request("clara.phase-connect.com")
    feed = r.feed_from_file("example_response.json")
    p = FeedParser()
    for post in feed:
        p.post(post)
        p.author()
        p.cid()
        p.embed()
        p.indexed_at()
        p.like_count()
        p.quote_count()
        p.record()
        p.record_text()
        p.reply_count()
        p.repost_count()
        p.uri()


def test_parser_record_text_from_request():
    r = Request("clara.phase-connect.com")
    feed = r.feed()
    p = FeedParser()
    for post in feed:
        p.post(post)
        p.author()
        p.cid()
        p.embed()
        p.indexed_at()
        p.like_count()
        p.quote_count()
        p.record()
        p.record_text()
        p.reply_count()
        p.repost_count()
        p.uri()
