import requests

for i in range(0, 1000):
    url = f"http://10.10.217.246/id/{i}"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.content.decode("utf-8"))