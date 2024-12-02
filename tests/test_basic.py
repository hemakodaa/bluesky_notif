from src.bluesky_notif.parser import Request, FeedParser


def test_request():
    Request("clara.phase-connect.com")


def test_parser_record_text_from_file():
    r = Request("clara.phase-connect.com")
    feeds = r.feed_from_file("example_response.json")
    p = FeedParser()
    for f in feeds:
        p.feed = f
        post = p.post()
        post.like_count()
        post.author()
        post.cid()
        post.embed()
        post.indexed_at()
        post.quote_count()
        post.record()
        post.record_text()
        post.repost_count()
        post.reply_count()
        post.uri()


def test_parser_record_text_from_request():
    r = Request("clara.phase-connect.com")
    feeds = r.feed()
    p = FeedParser()
    for f in feeds:
        p.feed = f
        post = p.post()
        post.like_count()
        post.author()
        post.cid()
        post.embed()
        post.indexed_at()
        post.quote_count()
        post.record()
        post.record_text()
        post.repost_count()
        post.reply_count()
        post.uri()
