import json
import httpx
from datetime import datetime


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
        # TODO: handle error if self._get() fails
        get = self._get()
        return get["feed"]


class FeedParser:
    def __init__(self):
        self._feed_post = None
        self._feed_reply = None
        self._feed_reason = None

    @property
    def post(self):
        if self._feed_post is None:
            raise ValueError("post is not set.")
        return self._feed_post

    @post.setter
    def post(self, feed: dict) -> dict:
        self._feed_post = feed.get("post")

    @property
    def reply(self) -> dict:
        return (
            {"error": "no_feed_reply"} if self._feed_reply is None else self._feed_reply
        )

    @reply.setter
    def reply(self, feed: dict) -> dict:
        self._feed_reply = feed.get("reply")

    @property
    def reason(self) -> dict:
        return self._feed_reason

    @reason.setter
    def reason(self, feed: dict) -> dict:
        self._feed_reason = feed.get("reason")

    @staticmethod
    def default_count(count) -> int:
        return 0 if count is None else count

    def reply_root(self) -> dict:
        return self.reply.get("root")

    def reply_parent(self) -> dict:
        return self.reply.get("parent")

    def reply_grandparentAuthor(self) -> dict:
        grandparent_author = self.reply.get("grandparentAuthor")
        return (
            {"error": "no_feed_reply_grandparentAuthor"}
            if grandparent_author is None
            else grandparent_author
        )

    def post_record_text(self):
        """
        The post's text.
        """
        return self.post_record().get("text")

    def post_uri(self) -> str:
        return self.post.get("uri")

    def post_cid(self) -> str:
        return self.post.get("cid")

    def post_author(self) -> dict:
        return self.post.get("author")

    def post_record(self) -> dict:
        """
        Contains the post's text
        """
        return self.post.get("record")

    def post_embed(self) -> dict:
        # not all posts have this
        embed = self.post.get("embed")
        return {"error": "no_embed"} if embed is None else embed

    def post_reply_count(self) -> int:
        count = self.post.get("replyCount")
        return FeedParser.default_count(count)

    def post_repost_count(self) -> int:
        count = self.post.get("repostCount")
        return FeedParser.default_count(count)

    def post_like_count(self) -> int:
        count = self.post.get("likeCount")
        return FeedParser.default_count(count)

    def post_quote_count(self) -> int:
        count = self.post.get("quoteCount")
        return FeedParser.default_count(count)

    def post_indexed_at(self):
        return datetime.fromisoformat(self.post.get("indexedAt"))
