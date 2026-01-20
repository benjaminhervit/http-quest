import requests
import time
import random

url = "http://127.0.0.1:5000/game/beg"
headers = {
    "content-type": "application/json",
    "authorization": "dev"
}
data = {"say": "please"}

# response = requests.get(url, headers=headers, json=data, timeout=10)
# data = response.json()
# for key, value in data.items():
#     print(f"{key}: {value}")
# print("-" * 50)

while True:
    try:
        response = requests.post(url, headers=headers, json=data)
        resp_data = response.json()
        
        try:
            print(resp_data["content"]['story'])
        except:
            print(resp_data["content"])
        # for k, v in resp_data.items():
        #     print(k, v)
        print("-" * 50)
    except (requests.RequestException, ValueError) as e:
        print(f"Error: {e}")
        print("-" * 50)

    sleep_time = 4 if random.random() < 0.45 else (5 if random.random() < 0.90 else random.uniform(2, 6))
    time.sleep(sleep_time)