import os
import argparse
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel

# Load environment variables
load_dotenv()
console = Console()

# Initialize Gemini Client (automatically picks up GEMINI_API_KEY from environment)
client = genai.Client()
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

def get_stock_price(ticker):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_KEY}"
    response = requests.get(url)
    data = response.json()
    if "Global Quote" in data and data["Global Quote"]:
        return data["Global Quote"]["05. price"], data["Global Quote"]["09. change"]
    return None, None

def generate_market_story(ticker, price, change, persona):
    trend = "up" if float(change) > 0 else "down"
    prompt = f"The stock {ticker} is currently trading at ${price}, and it is {trend} today. Tell a 3-sentence creative story about why this is happening. Speak in the persona of a {persona}."

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a creative storyteller interpreting financial data.",
            max_output_tokens=150,
        ),
    )
    return response.text.strip()

def main():
    parser = argparse.ArgumentParser(description="Market Bard: Creative Stock AI (Gemini Edition)")
    parser.add_argument("ticker", type=str, help="Stock ticker symbol (e.g., TSLA, NVDA)")
    parser.add_argument("--persona", type=str, default="Cyberpunk Hacker", help="Persona for the AI")
    args = parser.parse_args()

    console.print(f"[bold blue]Fetching data for {args.ticker.upper()}...[/bold blue]")
    price, change = get_stock_price(args.ticker.upper())

    if price:
        console.print(f"[bold green]Current Price: ${price} (Change: {change})[/bold green]")
        console.print(f"[bold yellow]Generating story as a {args.persona}...[/bold yellow]\n")
        story = generate_market_story(args.ticker.upper(), price, change, args.persona)
        console.print(Panel(story, title=f"{args.ticker.upper()} Story", expand=False))
    else:
        console.print("[bold red]Error fetching stock data. Check your ticker or API key.[/bold red]")

if __name__ == "__main__":
    main()
