import json
import httpx


class Request:
    APPVIEW = "https://public.api.bsky.app"
    ENDPOINT = "/xrpc/app.bsky.feed.getAuthorFeed"
    PARAMS = {"includePins": "true"}

    def __init__(self, bsky_at_identifier: str, limit_post=10):
        self.actor = bsky_at_identifier
        self.limit = limit_post

    def _get(self):
        Request.PARAMS["actor"] = self.actor
        Request.PARAMS["limit"] = self.limit
        with httpx.Client(params=Request.PARAMS) as client:
            r = client.get(Request.APPVIEW + Request.ENDPOINT, params=Request.PARAMS)
            return json.loads(r.text)

    def feed_from_file(self, filename: str):
        with open(filename, "r", encoding="utf-8") as file:
            read = json.load(file)
            return read["feed"]

    def feed(self):
        return self._get()["feed"]


class FeedParser:
    def __init__(self, feed: list):
        self._feed = feed

    def _post(self):
        for feed in self._feed:
            yield feed["post"]

    def record_text(self):
        """
        The post's text.
        """
        for record in self.record():
            yield record["text"]

    def uri(self):
        for post in self._post():
            yield post["uri"]

    def cid(self):
        for post in self._post():
            yield post["cid"]

    def author(self):
        for post in self._post():
            yield post["author"]

    def record(self):
        for post in self._post():
            yield post["record"]

    def embed(self):
        for post in self._post():
            yield post["embed"]

    def reply_count(self):
        for post in self._post():
            yield post["replyCount"]

    def repost_count(self):
        for post in self._post():
            yield post["repostCount"]

    def like_count(self):
        for post in self._post():
            yield post["likeCount"]

    def quote_count(self):
        for post in self._post():
            yield post["quoteCount"]

    def indexed_at(self):
        for post in self._post():
            yield post["indexedAt"]
