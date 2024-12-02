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

        # Possible values: [posts_with_replies, posts_no_replies, posts_with_media, posts_and_author_threads]
        Request.PARAMS["filters"] = ["posts_no_replies"]

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
    """
    There are three top-level objects for every item in a 'feed' list:
    1. Post (required, means it will always exist for every item)
    2. Reply
    3. Reason
    These three will determine what kind of post an Actor (Actor = an account on bsky) just posted, along with the filters used in Request.PARAMS

    A post that an actor writes, if it is NOT a reply or a repost, the item will NOT have a 'Reason' object. If an Actor reposted, that item will have a 'Post' and a 'Reason' object.

    If an item has a 'Reply' object, it means this item is a reply to another post. The layout of the 'Post' and the 'Reply' object goes like this:
    - 'Post' object contains information of the actor's reply. Makes sense, treating a reply as a 'post'.
    - 'Reply' object contains the conversations between the Actors. Inside the 'Reply' object, there are several properties. The original post is under the 'root' property, whereas the post whom the Actor replied to is under the 'parent' property. We can tell who the author of the original post is via the 'grandparentAuthor' property.
    """

    def __init__(self):
        self._feed_post = None
        self._feed_reply = None
        self._feed_reason = None
        self._feed = None

    @property
    def feed(self):
        return self._feed

    @feed.setter
    def feed(self, feed: dict):
        self._feed = feed
        self._feed_post = feed.get("post")
        self._feed_reply = feed.get("reply")
        self._feed_reason = feed.get("reason")

    @property
    def post(self):
        if self._feed_post is None:
            raise ValueError("post is not set.")
        return self._feed_post

    @property
    def reply(self) -> dict:
        return (
            {"error": "no_feed_reply"} if self._feed_reply is None else self._feed_reply
        )

    @property
    def reason(self) -> dict:
        """
        We can tell if a post is a repost or not through
        reason object
        """
        return self._feed_reason

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
