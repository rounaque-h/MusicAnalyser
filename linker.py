import json

import aiohttp


class Context:
    def __init__(self, client_name, client_version, visitor_data=None):
        self.client = Client(client_name, client_version, visitor_data)


class Client:
    def __init__(self, client_name, client_version, visitor_data=None):
        self.clientName = client_name
        self.clientVersion = client_version
        self.visitorData = visitor_data


class YouTube:
    def __init__(self):
        self.base_url = "https://music.youtube.com"
        self.key = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

    async def search(self, query, filter, continuation=None):
        url = f"{self.base_url}/youtubei/v1/search?key={self.key}&prettyPrint=false"
        headers = {"Content-Type": "application/json"}
        body = {
            "context": Context("WEB_REMIX", "1.20220328.01.00", "CgtsZG1ySnZiQWtSbyiMjuGSBg%3D%3D"),
            "query": query,
            "params": filter,
        }
        if continuation:
            body["continuation"] = continuation

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as response:
                data = await response.json()

        items = []
        continuation_token = None

        if "contents" in data:
            contents = data["contents"]
            tabbed_results = contents["tabbedSearchResultsRenderer"]["tabs"]
            if len(tabbed_results) > 0:
                content = tabbed_results[0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0][
                    "musicShelfRenderer"
                ]
                items = self.extract_items(content)

        if "continuationContents" in data:
            continuation_contents = data["continuationContents"]["musicShelfContinuation"]
            continuation_token = continuation_contents["continuations"][0]["nextRadioContinuationData"]["continuation"]

        return {"items": items, "continuation": continuation_token}

    def extract_items(self, content):
        items = []
        for item in content["contents"]:
            if "musicResponsiveListItemRenderer" in item:
                renderer = item["musicResponsiveListItemRenderer"]
                item_type = renderer.get("flexColumns", [])[0].get("musicResponsiveListItemFlexColumnRenderer", {}).get(
                    "text", {}
                ).get("runs", [])[0].get("text", "")
                if item_type == "Song":
                    song_info = renderer["navigationEndpoint"]["watchEndpoint"]
                    song_authors = self.extract_authors(renderer.get("subtitle", {}).get("runs", []))
                    song_album = self.extract_album(renderer.get("subtitle", {}).get("runs", []))
                    thumbnail = renderer["thumbnail"]["thumbnails"][0]
                    duration_text = renderer.get("lengthText", {}).get("runs", [])[0].get("text", "?")
                    item = {
                        "type": "song",
                        "info": song_info,
                        "authors": song_authors,
                        "album": song_album,
                        "thumbnail": thumbnail,
                        "durationText": duration_text,
                    }
                    items.append(item)
        return items

    def extract_authors(self, runs):
        authors = []
        for run in runs:
            if "navigationEndpoint" in run:
                authors.append(run["navigationEndpoint"]["browseEndpoint"])
        return authors

    def extract_album(self, runs):
        album = None
        for run in runs:
            if "navigationEndpoint" in run:
                album = run["navigationEndpoint"]["browseEndpoint"]
        return album


