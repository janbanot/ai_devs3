# Task S01E01
import os
from dotenv import load_dotenv
from openai import OpenAI
from playwright.sync_api import sync_playwright

load_dotenv()
xyz_url = os.getenv("XYZ_URL")
username = os.getenv("XYZ_LOGIN")
password = os.getenv("XYZ_PASSWORD")
client = OpenAI()


def call_llm_api(question_text: str) -> str:
    prompt = f"Answer the following question: {question_text}. Provide just the number, nothing else."
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


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(xyz_url)
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    human_question_text = page.text_content("#human-question")
    answer = call_llm_api(human_question_text)
    page.fill("input[name=answer]", answer)
    page.click("button[type=submit]")
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
