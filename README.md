# getAuhorFeed

The `GET` endpoint `/xrpc/app.bsky.feed.getAuthorFeed` provides a view of an account's 'author feed' (posts, reposts, replies, etc) made by the account. It requires no auth.

The complete definition model is available at AT Protocol SDK under [app.bsky.feed.get_author_feed](https://atproto.blue/en/latest/atproto/atproto_client.models.app.bsky.feed.get_author_feed.html)

This repo is meant to make things easier for me to automate post notifications from select accounts I follow, let's see how it goes.

# High-level overview
Every 'feed' is a list, which items consists of 'post' (required), 'reply' (optional), and 'reason' (optional). Each item represent a post.
Combinations of these or their properties determine what kind of post the account made. For now, see this [function](https://github.com/hemakodaa/bsky-getAuthorFeed-parser/blob/ea1fc5d6155767c93ec74f52053645cbe40533bb/src/bluesky_notif/parser.py#L377-L399)'s comments for a better idea.