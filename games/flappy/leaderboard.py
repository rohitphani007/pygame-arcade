import requests

DB_URL = "https://flappy-scores-ec9d5-default-rtdb.firebaseio.com/flappy_scores.json"

def submit_score(name, score):
    package = {"name": name, "score": score}
    try:
        requests.post(DB_URL, json=package, timeout=5)
    except:
        pass

def get_top_scores():
    try:
        response = requests.get(DB_URL, timeout=5)
        if response.text == "null":
            return []
        data = response.json()
        score_list = [info for info in data.values()]
        score_list.sort(key=lambda x: x['score'], reverse=True)
        return score_list[:5]
    except:
        return []