import os, base64, json, re
from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()
KEY = os.environ.get("GEMINI_API_KEY", "")
PASSWORD = os.environ.get("APP_PASSWORD", "")
MODEL = os.environ.get("MODEL", "gemini-2.5-flash")

PROMPT = """This is a handwritten order for a veterinary medical shop in India (Hindi/English/Marathi names possible). Read every line. Ignore struck-through lines and the heading (return the heading as "customer"). Each line is usually a product name followed by a quantity; numbers may also be strip size, so note ambiguity.
Return ONLY JSON: {"customer":"","items":[{"raw":"literal reading","item":"best product name","qty":number or null,"note":"short note if ambiguous or empty","confident":true/false}]}
"""

@app.post("/api/read")
def read(image: UploadFile = File(...), products: str = Form(""), x_password: str = Header("")):
    if PASSWORD and x_password != PASSWORD:
        raise HTTPException(401, "bad password")
    data = base64.b64encode(image.file.read()).decode()
    plist = ("Shop product list (match to these when a scribble is close; otherwise keep your best reading):\n" + products) if products.strip() else "No product list available."
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        headers={"x-goog-api-key": KEY},
        json={"contents": [{"parts": [{"text": PROMPT + plist},
              {"inline_data": {"mime_type": "image/jpeg", "data": data}}]}],
              "generationConfig": {"responseMimeType": "application/json"}},
        timeout=90)
    if r.status_code == 429:
        raise HTTPException(429, "free limit reached, try later")
    r.raise_for_status()
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise HTTPException(502, "unreadable reply")
    return json.loads(m.group(0))

app.mount("/", StaticFiles(directory="static", html=True), name="static")
