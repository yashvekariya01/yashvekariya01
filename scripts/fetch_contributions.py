import os
import json
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    
    if res.status_code != 200:
        print("Failed to fetch contributions")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    days = soup.find_all("td", class_="ContributionCalendar-day")
    
    contrib_data = []
    for day in days:
        date = day.get("data-date")
        count = day.get("data-level", "0")
        if date:
            contrib_data.append({"date": date, "level": int(count)})
            
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(contrib_data, f)
    print("data/contributions.json saved!")

if __name__ == "__main__":
    fetch_contributions("yashvekariya01")