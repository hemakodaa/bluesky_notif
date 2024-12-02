from parser import Request, FeedParser
import json


def main():
    r = Request("clara.phase-connect.com")
    feed = r.feed()
    p = FeedParser()
    with open("test.json", "w") as file:
        file.write(json.dumps({"feed": feed}))


if __name__ == "__main__":
    main()
