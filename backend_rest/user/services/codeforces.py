import requests

def fetch_CFData(username):
    try:
        url1= f"https://codeforces.com/api/user.info?handles={username}"
        url2=f"https://codeforces.com/api/user.status?handle={username}&from=1&count=100"
        res1 = requests.get(url1, timeout=5)
        res2 = requests.get(url2, timeout=5)

        res1.raise_for_status()
        res2.raise_for_status()

        user_info = res1.json()
        submissions = res2.json()

        solved_problems = set()

        for sub in submissions["result"]:
            if sub["verdict"] == "OK":
                problem_id = f'{sub["problem"]["contestId"]}-{sub["problem"]["index"]}'
                solved_problems.add(problem_id)

        total_solved = len(solved_problems)

        return {
            "user": user_info["result"][0],
            "totalSolved": total_solved,
            "submissions": submissions["result"]
        }


    except requests.exceptions.RequestException as e:
        return {"error": str(e)}