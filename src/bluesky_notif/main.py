from parser import Request, FeedParser
import json


def main():
    r = Request("clara.phase-connect.com", 1)
    feeds = r.feed()
    p = FeedParser()
    for f in feeds:
        p.feed = f
        print(p.post_record_text())
    # with open("test.json", "w") as file:
    #     file.write(json.dumps({"feed": feed}))


if __name__ == "__main__":
    main()
