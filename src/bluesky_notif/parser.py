import json
import httpx


class Request:
    APPVIEW = "https://public.api.bsky.app"
    ENDPOINT = "/xrpc/app.bsky.feed.getAuthorFeed"
    PARAMS = {"includePins": "true"}

    def __init__(self, bsky_at_identifier: str, limitpost=10):
        self.actor = bsky_at_identifier
        self.limit = limitpost

    def _get(self):
        Request.PARAMS["actor"] = self.actor
        Request.PARAMS["limit"] = self.limit
        # TODO: add request error handling
        with httpx.Client(params=Request.PARAMS) as client:
            r = client.get(Request.APPVIEW + Request.ENDPOINT, params=Request.PARAMS)
            return json.loads(r.text)

    def feed_from_file(self, filename: str):
        with open(filename, "r", encoding="utf-8") as file:
            read = json.load(file)
            return read["feed"]

    def feed(self) -> list:
        return self._get()["feed"]


class FeedParser:
    def __init__(self):
        self.feed = None

    @property
    def post(self):
        if self.feed is None:
            raise ValueError("feed is type None. Author's feed is empty")
        return self.feed

    @post.setter
    def post(self, post: dict):
        self.feed = post["post"]

    def record_text(self):
        """
        The post's text.
        """
        return self.record()["text"]

    def uri(self):
        return self.post["uri"]

    def cid(self):
        return self.post["cid"]

    def author(self):
        return self.post["author"]

    def record(self):
        """
        Contains the post's text
        """
        return self.post["record"]

    def embed(self):
        # not all posts have this
        try:
            return self.post["embed"]
        except KeyError:
            return {"error": "no_embed"}

    def reply_count(self):
        return self.post["replyCount"]

    def repost_count(self):
        return self.post["repostCount"]

    def like_count(self):
        return self.post["likeCount"]

    def quote_count(self):
        return self.post["quoteCount"]

    def indexed_at(self):
        return self.post["indexedAt"]
