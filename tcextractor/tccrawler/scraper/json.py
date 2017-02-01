

def create_json(meta):
    data = {
        "Url": meta["url"],
        "Title": meta["title"],
        "Description": meta["description"],
        "Author": {
            "Name": meta["author"],
            "Url": meta["author_url"],
        },
        "Image": meta["image"],
        "Embed": {
            "Code": meta["code"],
            "Poster": "" if meta["video"] == ("",) else meta["image"],
        },
        "audio": meta["audio"],
        "time": meta["time"],
        # "raw_data": meta["raw"],
    }
    return data



