import json
import requests

fileJSON = 'result.json'


def format_JSON(obj):
    try:
        r = requests.get("https://wbx-content-v2.wbstatic.net/ru/" + obj + ".json")
        with open(fileJSON, 'w', encoding="utf-8") as f:
            json.dump(r.json(), f, ensure_ascii=False, sort_keys=True, indent=4)
    except:
        pass
