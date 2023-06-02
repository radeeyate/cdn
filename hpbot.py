import requests

import json

quote = requests.get("https://api.portkey.uk/quote").json()

book = quote["story"]

author = quote["speaker"]

quote = quote["quote"]

print(f"{quote} -{author} ({book})")

authJson = {"Authorization": ""}

post = requests.post("https://api.wasteof.money/posts", headers = authJson, json = {"post": f"{quote} -{author} ({book})"})

print(post.json())
