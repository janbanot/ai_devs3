import os
import requests
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
centrala_url = os.getenv("CENTRALA_URL")
api_key = os.getenv("AI_DEVS_API_KEY")
client = OpenAI()

TASK_NAME = "JSON"
json_url = f"{centrala_url}/data/{api_key}/json.txt"
report_url = f"{centrala_url}/report"


def get_data(url: str) -> str:
    response = requests.get(url)
    return response.text


def post_answer(answer: str) -> str:
    answer_json = {
        "task": TASK_NAME,
        "apikey": api_key,
        "answer": answer
    }
    response = requests.post(report_url, json=answer_json)
    return response.json()["message"]


def call_llm_api(prompt: str) -> str:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )
    return chat_completion.choices[0].message.content


def process_json_data(data):
    test_data = data.get('test-data', [])

    for item in test_data:
        if 'test' in item:
            question = item['test']['q']
            answer = call_llm_api(f"Answer this question: {question}")
            item['test']['a'] = answer
            continue

        question = item['question']
        given_answer = item['answer']

        try:
            a, b = map(int, question.split(' + '))
            correct_answer = a + b

            if given_answer != correct_answer:
                item['answer'] = correct_answer

        except ValueError:
            print(f"Special question found: {question}")


if __name__ == "__main__":
    data = json.loads(get_data(json_url))
    data['apikey'] = api_key

    process_json_data(data)

    response = post_answer(data)
    print(response)
