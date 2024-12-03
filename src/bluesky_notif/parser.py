import json
import httpx
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from collections.abc import Generator, Iterator


class ReplyType(Enum):
    POST_VIEW = "app.bsky.feed.defs#postView"
    NOT_FOUND_POST = "app.bsky.feed.defs#notFoundPost"
    BLOCKED_POST = "app.bsky.feed.defs#blockedPost"


class ReasonType(Enum):
    REPOST = "app.bsky.feed.defs#reasonRepost"
    PIN = "app.bsky.feed.defs#reasonPin"
    NONE = ""


class EmbedType(Enum):
    IMAGES = "app.bsky.embed.images#view"
    VIDEO = "app.bsky.embed.video#view"
    EXTERNAL = "app.bsky.embed.external#view"
    RECORD = "app.bsky.embed.record#view"
    RECORD_WITH_MEDIA = "app.bsky.embed.recordWithMedia#view"
    NONE = ""


class FacetType(Enum):
    LINK = "app.bsky.richtext.facet#link"
    TAG = "app.bsky.richtext.facet#tag"
    NONE = ""


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
        Request.PARAMS["filter"] = ["posts_no_replies"]

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


@dataclass
class PostRecord:
    _record: dict

    def record_type(self):
        return self._record.get("$type")

    def text(self):
        """
        The post's text.
        """
        return self._record.get("text")

    def created_at(self):
        return self._record.get("createdAt")

    def embed(self):
        return self._record.get("embed")

    def facets(self) -> Generator[FacetType | dict[str, FacetType | str]]:
        facet: list | None = self._record.get("facets")
        if not facet:
            return FacetType.NONE
        for item in facet:
            features: list | None = item.get("features")
            for f in features:
                match f.get("$type"):
                    case FacetType.LINK.value:
                        yield {"type": FacetType.LINK, "uri": f.get("uri")}
                    case FacetType.TAG.value:
                        pass
                    case _:
                        yield {"type": FacetType.NONE, "uri": ""}

    def langs(self):
        return self._record.get("langs")


@dataclass
class PostAuthor:
    _author: dict

    def did(self):
        return self._author.get("did")

    def handle(self):
        return self._author.get("handle")

    def display_name(self):
        return self._author.get("displayName")

    def avatar(self):
        return self._author.get("avatar")

    def labels(self):
        return self._author.get("labels")

    def created_at(self):
        return self._author.get("createdAt")


@dataclass
class EmbedTypeImage:
    _images: dict

    def thumbnail(self):
        return self._images.get("thumb")

    def fullsize(self):
        return self._images.get("fullsize")

    def alt_text(self):
        return self._images.get("alt")


class PostEmbedImage(Iterator):
    def __init__(self, embed: dict):
        super().__init__()
        self._embed_images: list = embed.get("images")

    def __next__(self) -> EmbedTypeImage:
        try:
            item: dict = self._embed_images.pop(0)
            return EmbedTypeImage(item)
        except IndexError:
            raise StopIteration


@dataclass
class PostParser:
    _post: dict

    @staticmethod
    def _default_count(count) -> int:
        return 0 if count is None else count

    def uri(self) -> str:
        return self._post.get("uri")

    def cid(self) -> str:
        return self._post.get("cid")

    def author(self) -> PostAuthor:
        return PostAuthor(self._post.get("author"))

    def record(self) -> PostRecord:
        """
        Contains the post's text
        """
        return PostRecord(self._post.get("record"))

    def embed(self) -> Iterator[EmbedTypeImage] | None:
        # not all posts have this
        # TODO: determine what type the embed is with EmbedType, and return the corresponding class/dataclass
        embed: dict | None = self._post.get("embed")
        if not embed:
            return None
        embed_type = embed.get("$type")
        match embed_type:
            # a custom return container type may be necessary for this match case, containing the type and the relevant information
            case EmbedType.IMAGES.value:
                return PostEmbedImage(embed)
            case _:
                return None  # placeholder

    def reply_count(self) -> int:
        count = self._post.get("replyCount")
        return PostParser._default_count(count)

    def repost_count(self) -> int:
        count = self._post.get("repostCount")
        return PostParser._default_count(count)

    def like_count(self) -> int:
        count = self._post.get("likeCount")
        return PostParser._default_count(count)

    def quote_count(self) -> int:
        count = self._post.get("quoteCount")
        return PostParser._default_count(count)

    def indexed_at(self):
        return datetime.fromisoformat(self._post.get("indexedAt"))


class ReplyParser:
    def __init__(self, reply: dict):
        self._r = reply

    def _reply(self):
        return self._r

    def root(self) -> dict:
        return self._reply().get("root")

    def parent(self) -> dict:
        return self._reply().get("parent")

    def grandparent_author(self) -> dict:
        grandparent_author = self._reply().get("grandparentAuthor")
        return (
            {"error": "no_feed_reply_grandparentAuthor"}
            if grandparent_author is None
            else grandparent_author
        )


class ReasonParser:
    def __init__(self, reason: dict | None):
        self._r = reason

    def _reason(self) -> dict | None:
        return {"$type": "", "by": "", "indexedAt": ""} if self._r is None else self._r

    def reason_type(self) -> ReasonType:
        t = self._reason().get("$type")
        if not t:
            return ReasonType.NONE
        match t:
            case ReasonType.REPOST.value:
                return ReasonType.REPOST
            case ReasonType.PIN.value:
                return ReasonType.PIN

    def by(self):
        b = self._reason().get("by")
        return "" if not b else b

    def indexed_at(self):
        i = self._reason().get("indexedAt")
        return "" if not i else datetime.fromisoformat(i)


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

    def post(self):
        if self._feed_post is None:
            raise ValueError("feed is not set.")
        return PostParser(self._feed_post)

    def reply(self) -> ReplyParser:
        return (
            ReplyParser({"error": "no_feed_reply"})
            if self._feed_reply is None
            else ReplyParser(self._feed_reply)
        )

    def reason(self) -> ReasonParser:
        """
        We can tell if a post is a repost or not through
        reason object
        """
        return ReasonParser(self._feed_reason)
