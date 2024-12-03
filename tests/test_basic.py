from src.bluesky_notif.parser import (
    Request,
    FeedParser,
    PostEmbedExternal,
    PostEmbedImageIterator,
    PostEmbedRecord,
    PostEmbedVideo,
    PostEmbedRecordWithMedia,
)


def test_request():
    Request("clara.phase-connect.com")


def parser(p: FeedParser, feeds: dict):
    for f in feeds:
        p.feed = f
        post = p.post()

        author = post.author()
        author.avatar()
        author.created_at()
        author.did()
        author.display_name()
        author.handle()
        author.labels()

        post.like_count()
        post.cid()
        post.indexed_at()
        post.quote_count()
        post.repost_count()
        post.reply_count()
        post.uri()

        post_record = post.record()
        post_record.text()
        post_record.record_type()
        post_record.created_at()
        post_record.embed()
        post_record.langs()
        post_record.facets()

        reply = p.reply()
        reply.grandparent_author()
        reply.parent()
        reply.root()

        reason = p.reason()
        reason.by()
        reason.indexed_at()
        reason.reason_type()

        embed = post.embed()
        if embed is None:
            continue
        match embed:
            case PostEmbedImageIterator():
                for image in embed:
                    print(image)
            case PostEmbedVideo():
                embed.cid()
                embed.alt_text()
                embed.aspect_ratio()
                embed.playlist()
                embed.thumbnail()
            case PostEmbedExternal():
                embed.description()
                embed.thumbnail()
                embed.title()
                embed.uri()
            case PostEmbedRecord():
                embed.record()
            case PostEmbedRecordWithMedia():
                embed.media()


def test_parser_record_text_from_file():
    r = Request("clara.phase-connect.com")
    feeds = r.feed_from_file("example_response.json")
    p = FeedParser()
    parser(p, feeds)


def test_parser_record_text_from_request():
    r = Request("clara.phase-connect.com")
    feeds = r.feed()
    p = FeedParser()
    parser(p, feeds)
