import os
import requests
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
centrala_url = os.getenv("CENTRALA_URL")
api_key = os.getenv("AI_DEVS_API_KEY")
client = OpenAI()

TASK_NAME = "CENZURA"
input_url = f"{centrala_url}/data/{api_key}/cenzura.txt"
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


if __name__ == "__main__":
    input_data = get_data(input_url)
    print(input_data)

    prompt = f"""
    Act as a censor and censor the given text.
    Replace all occurences of the defined terms with the word "CENZURA".
    Return only the censored text. Nothing more.
    You should replace following terms:
    - name
    - surname
    - address (street name and number)
    - city name
    - age

    <example>
    - Input: Podejrzany nazywa się Tomasz Kaczmarek. Jest zameldowany w Poznaniu, ul. Konwaliowa 18. Ma 25 lat.
    - Output: Podejrzany nazywa się CENZURA. Jest zameldowany w CENZURA, ul. CENZURA. Ma CENZURA lat.
    </example>

    {{TEXT}}
    {input_data}
    """
    censored_data = call_llm_api(prompt)
    print(censored_data)

    response = post_answer(censored_data)
    print(response)
