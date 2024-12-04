from parser import Request, FeedParser
import json


def main():
    r = Request("clara.phase-connect.com", 20)
    feeds = r.feed_from_file("posts_no_replies.json")
    p = FeedParser()
    for f in feeds:
        p.feed = f
        print(p.determine_post_kind())
    # for f in feeds:
    #     p.feed = f
    #     post = p.post()
    #     embed = post.embed()
    #     if embed is None:
    #         continue
    #     for image in embed:
    #         print(image.thumbnail())

    # with open("posts_no_replies.json", "w") as file:
    #     file.write(json.dumps({"feed": feeds}))


if __name__ == "__main__":
    main()
