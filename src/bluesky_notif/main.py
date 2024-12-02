from parser import Request, FeedParser


def main():
    r = Request("clara.phase-connect.com")
    for post in FeedParser(r.feed()).record_text():
        print(post)


if __name__ == "__main__":
    main()
