import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
xyz_url = os.getenv("XYZ_URL")
client = OpenAI()
