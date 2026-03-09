from openai import OpenAI
from pydantic import BaseModel
from src.prompts import THEME_EXTRACTION_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_structured_response(prompt, text_format: type[BaseModel], system_message, model = "gpt-5-nano", reasoning_effort: str = "low"):
    response = client.responses.parse(
        model=model,
        reasoning={"effort": reasoning_effort},
        input=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        text_format=text_format,
    )
    return response.output_parsed