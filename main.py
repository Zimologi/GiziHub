from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

class MealInput(BaseModel):
    meal: str

DEESEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEESEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

PROMPT_TEMPLATE = """
Saya ingin kamu menganalisis makanan berikut dalam konteks nutrisi Indonesia. Tolong hitung estimasi kalori dan protein (dalam gram) untuk makanan ini.

Makanan: {meal}

Tampilkan dalam format:
- Kalori: [angka] kkal
- Protein: [angka] gram
"""

@app.post("/analyze")
async def analyze_meal(input: MealInput):
    prompt = PROMPT_TEMPLATE.format(meal=input.meal)
    headers = {
        "Authorization": f"Bearer {DEESEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Kamu adalah ahli gizi Indonesia."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(DEESEEK_API_URL, headers=headers, json=payload)
        result = response.json()

    output = result['choices'][0]['message']['content']
    return {"result": output}