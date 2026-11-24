# Order Reader (100% free version)

Uses Google Gemini free tier (reads handwriting) + Render free hosting.

## 1. Free API key
Go to aistudio.google.com -> Sign in with Google -> "Get API key" -> Create key. No card needed.

## 2. Put code on GitHub (free)
New repo, upload all these files (keep the `static` folder).

## 3. Host free on Render
render.com -> New -> Web Service -> connect repo.
Build: pip install -r requirements.txt
Start: uvicorn server:app --host 0.0.0.0 --port $PORT
Environment variables:
  GEMINI_API_KEY = your key
  APP_PASSWORD   = any password you choose

## 4. Install on Android
Open your Render URL in Chrome -> three dots -> Install app.

Notes: the free tier has daily limits (fine for a shop's daily orders) and Render's free plan sleeps when idle (first open may take ~30 seconds). Free-tier data may be used by Google to improve products, so avoid customer private details.
