from src.bluesky_notif.parser import Request, FeedParser


def test_request():
    Request("clara.phase-connect.com")


def test_parser_record_text_from_file():
    r = Request("clara.phase-connect.com")
    feed = r.feed_from_file("example_response.json")
    p = FeedParser()
    for post in feed:
        p.post = post
        p.reply = post
        p.reason = post
        p.reply_grandparentAuthor()
        p.reply_parent()
        p.reply_root()
        p.post_author()
        p.post_cid()
        p.post_embed()
        p.post_indexed_at()
        p.post_like_count()
        p.post_quote_count()
        p.post_record()
        p.post_record_text()
        p.post_reply_count()
        p.post_repost_count()
        p.post_uri()


def test_parser_record_text_from_request():
    r = Request("clara.phase-connect.com")
    feed = r.feed()
    p = FeedParser()
    for post in feed:
        p.post = post
        p.reply = post
        p.reason = post
        p.reply_grandparentAuthor()
        p.reply_parent()
        p.reply_root()
        p.post_author()
        p.post_cid()
        p.post_embed()
        p.post_indexed_at()
        p.post_like_count()
        p.post_quote_count()
        p.post_record()
        p.post_record_text()
        p.post_reply_count()
        p.post_repost_count()
        p.post_uri()
