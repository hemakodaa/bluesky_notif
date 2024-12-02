import json


def read_file():
    with open("example_response.json", "r", encoding="utf-8") as file:
        return json.load(file)


def feed_parser():
    """
    This parses "/xrpc/app.bsky.feed.getAuthorFeed" endpoint
    """
    read = read_file()
    feed: list = read["feed"]
    first_feed = feed[
        0
    ]  # for purposes of making this parser only, should be named something else

    # should it parse everything or only information of interest?
    post: dict = first_feed["post"]
    uri = post["uri"]
    cid = post["cid"]
    author = post["author"]
    record = post["record"]  # this is where the text of the bsky post is
    embed = post["embed"]
    reply_count = post["replyCount"]
    repost_count = post["repostCount"]
    like_count = post["likeCount"]
    quote_count = post["quoteCount"]
    indexed_at = post["indexedAt"]
    # print(record["text"])
