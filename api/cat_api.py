import requests

def get_random_cat():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        return response.json()[0]['url']
    return "Couldn't fetch a cat right now."

def get_cat_fact():
    url = "https://catfact.ninja/fact"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("fact", "Couldn't find a cat fact 😿")
        else:
            return "😿 Couldn't fetch a cat fact at the moment."
    except Exception as e:
        print(f"Error fetching cat fact: {e}")
        return "Something went wrong trying to get a cat fact."
