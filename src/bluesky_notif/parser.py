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

    def post(self, feed: dict):
        """
        This method mutates, maybe find a better way
        """
        self.feed = feed["post"]
        if self.feed is None:
            raise ValueError("feed is type None. Author's feed is empty")
        

    def record_text(self):
        """
        The post's text.
        """
        return self.record()["text"]

    def uri(self):
        return self.feed["uri"]

    def cid(self):
        return self.feed["cid"]

    def author(self):
        return self.feed["author"]

    def record(self):
        """
        Contains the post's text
        """
        return self.feed["record"]

    def embed(self):
        # not all posts have this
        try:
            return self.feed["embed"]
        except KeyError:
            return {"error": "no_embed"}

    def reply_count(self):
        return self.feed["replyCount"]

    def repost_count(self):
        return self.feed["repostCount"]

    def like_count(self):
        return self.feed["likeCount"]

    def quote_count(self):
        return self.feed["quoteCount"]

    def indexed_at(self):
        return self.feed["indexedAt"]
