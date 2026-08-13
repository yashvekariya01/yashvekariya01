#!/usr/bin/env python3
import os
import json
import requests
import re
from bs4 import BeautifulSoup

def fetch_contributions(username="yashvekariya01"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching contributions from: {url}")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Error: Failed to fetch contributions page. Status: {res.status_code}")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    
    # Extract total contributions in the last year
    total_contributions = 0
    for h2 in soup.find_all("h2"):
        txt = h2.get_text()
        if "contributions" in txt:
            # Matches strings like "53 contributions in the last year" or "1,234 contributions"
            match = re.search(r'([\d,]+)\s+contributions', txt, re.IGNORECASE)
            if match:
                total_contributions = int(match.group(1).replace(",", ""))
                break

    # Extract days
    days = soup.find_all("td", class_="ContributionCalendar-day")
    contrib_data = []
    
    for day in days:
        date = day.get("data-date")
        level = day.get("data-level")
        if date and level is not None:
            contrib_data.append({
                "date": date,
                "level": int(level)
            })

    result = {
        "total_contributions": total_contributions,
        "days": contrib_data
    }

    # Ensure output dir exists
    os.makedirs("data", exist_ok=True)
    
    # Save to file
    output_path = "data/contributions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print(f"Saved contributions index to {output_path}!")
    print(f"Total Contributions: {total_contributions}")
    print(f"Total Days Scraped: {len(contrib_data)}")

if __name__ == "__main__":
    fetch_contributions()