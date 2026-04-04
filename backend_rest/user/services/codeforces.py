import requests
import time
from redis_client import redis_client
import json
CACHE_TTL=24*60*60
from collections import defaultdict
from datetime import datetime, timedelta

def build_cf_heatmap(submissions):
    heatmap = defaultdict(int)

    one_year_ago = datetime.utcnow() - timedelta(days=365)

    for sub in submissions:
        if sub.get("verdict") != "OK":
            continue

        ts = sub.get("creationTimeSeconds")
        date_obj = datetime.utcfromtimestamp(ts)

        # ✅ only last 1 year
        if date_obj < one_year_ago:
            continue

        date = date_obj.strftime("%Y-%m-%d")
        heatmap[date] += 1

    return dict(heatmap)
def fetch_CFData(username):
    try:
  
        key=f"cf_{username}"
        data=redis_client.get(key)
        if data:
            print("Returning cached CF data 🔥")
            return json.loads(data)

        print("Fetching new CF data...")
        url1= f"https://codeforces.com/api/user.info?handles={username}"
        url2=f"https://codeforces.com/api/user.status?handle={username}&from=1&count=1500"
        res1 = requests.get(url1, timeout=5)
        res2 = requests.get(url2, timeout=5)

        res1.raise_for_status()
        res2.raise_for_status()

        user_info = res1.json()
        submissions = res2.json()
        total_submissions = len(submissions["result"])
        solved_problems = set()

        for sub in submissions["result"]:
            if sub["verdict"] == "OK":
                problem_id = f'{sub["problem"]["contestId"]}-{sub["problem"]["index"]}'
                solved_problems.add(problem_id)

        total_solved = len(solved_problems)
        now = time.time()
        cf_heatmap = build_cf_heatmap(submissions["result"])
        data={
             "user": user_info["result"][0],
            "totalSolved": total_solved,
            "totalSubmissions":total_submissions,
            "heatmap": cf_heatmap
        }
        redis_client.setex( 
            key,
            CACHE_TTL,
            json.dumps(data)
        )
       

        return data


    except requests.exceptions.RequestException as e:
        return {"error": str(e)}