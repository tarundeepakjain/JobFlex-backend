import requests

def fetch_leetcodeData(username):
    try:
        url = f"https://alfa-leetcode-api.onrender.com/{username}/profile"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}