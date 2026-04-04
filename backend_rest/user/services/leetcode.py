import requests
import time
import json
import pandas as pd
from redis_client import redis_client

CACHE_TTL = 60 * 60 * 24
def filter_data(data):
 return {
        "totalSolved": data.get("totalSolved"),
        "totalSubmissions": data.get("totalSubmissions"),
        "totalQuestions": data.get("totalQuestions"),
        "ranking": data.get("ranking"),
        "submissionCalendar": data.get("submissionCalendar"),
    }

def fetch_leetcodeData(username):
    try:
        now=time.time()
        key=f"lc_{username}"
        data=redis_client.get(key)
        if data:
            print("Returning cached LC data 🔥")
            return json.loads(data)

        print("Fetching new LC data...")

        url = f"https://alfa-leetcode-api.onrender.com/{username}/profile"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
      
        data = filter_data(response.json())
        if not data:
          return {"error": "Invalid response from LeetCode API"}
        redis_client.setex(
            key,
            CACHE_TTL,
            json.dumps(data)
        )
        
        return data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}