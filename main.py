import requests

#Notion requires a setup before it becomes functional. Please read the API reference https://developers.notion.com/docs/getting-started
DATABASE_ID = ""
TOKEN = ""
url_get = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
payload = {"page_size": 25}

headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "authorization": f"{TOKEN}"
}

#Get the current data and format it into JSON
response = requests.post(url_get, json=payload, headers=headers)
jsond = response.json()
len_items = len(jsond["results"])


#Get all required data and assign it to vars
for a in range(len_items):
    props = jsond["results"][a]["properties"]

    done = props["Done?"]["checkbox"]
    longest_streak = int(props["Longest Streak"]["number"])
    num = int(props["Streak"]["number"])
    page_id = jsond["results"][a]["id"]
    days_from_start = int(props["Days from start"]["number"])
    days_hit = int(props["Days hit"]["number"])

    days_from_start += 1

    #Check if the habit was done
    if done:
            num += 1
            days_hit += 1
    else:
        num = 0
    
    #Check if the current streak is the longest streak
    if num > longest_streak:
        longest_streak = num
    accuracy = round(days_hit/days_from_start, 2)
    
    payload_patch = {
        "properties": {
            "Streak": {"number": num},
            "Accuracy": {"number": accuracy},
            "Longest Streak": {"number": longest_streak},
            "Days from start": {"number": days_from_start},
            "Days hit": {"number": days_hit},
            "Done?": {"checkbox": False}
        }
    }
    
    #Send the update
    url_patch = f"https://api.notion.com/v1/pages/{page_id}"
    sent = requests.patch(url=url_patch, json=payload_patch, headers=headers)
