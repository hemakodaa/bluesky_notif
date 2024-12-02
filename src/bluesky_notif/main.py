import httpx

APPVIEW = "https://public.api.bsky.app"
ENDPOINT = "/xrpc/app.bsky.feed.getAuthorFeed"
ACTOR = "clara.phase-connect.com"
PARAMS = {"actor": ACTOR, "limit": 10, "includePins": "true"}


def main():
    with httpx.Client(params=PARAMS) as client:
        r = client.get(APPVIEW + ENDPOINT, params=PARAMS)
        html = r.text()
        # with open("example_response.json", "w+", encoding="utf-8") as file:
        #     file.write(html)


if __name__ == "__main__":
    main()
