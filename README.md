# 🎭 Market Bard (Agents League - Creative Apps Track)

**Market Bard** is a creative CLI application built for the Microsoft Agents League (Creative Apps Track). It transforms dry financial data into entertaining micro-fiction using AI.

## How it works
The app takes a stock ticker and a "Persona" as arguments. It fetches the real-time stock price and passes that data to Google's Gemini AI, which acts as a specialized Agent to generate a 3-sentence story explaining the stock's market movement in that persona.

## Setup
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with `GEMINI_API_KEY` and `ALPHA_VANTAGE_KEY`.
4. Run: `python app.py NVDA --persona "1920s Gangster"`
