import os
import requests
from dotenv import load_dotenv
from typing import List


load_dotenv()
api_key = os.getenv("AI_DEVS_API_KEY")
poligon_url = os.getenv("POLIGON_URL")
TASK_NAME = "POLIGON"


def get_data() -> str:
    url = f"{poligon_url}/dane.txt"
    response = requests.get(url)
    return response.text


def post_answer(answer: List[str]) -> str:
    url = f"{poligon_url}/verify"
    answer_json = {
        "task": TASK_NAME,
        "apikey": api_key,
        "answer": answer
    }
    response = requests.post(url, json=answer_json)
    return response.json()["message"]


if __name__ == "__main__":
    task_data = get_data()
    data_list = task_data.splitlines()
    response = post_answer(data_list)
    print(response)
