import os
from groq import Groq
from tavily import TavilyClient

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

REALTIME_KEYWORDS = [
    "today", "latest", "current", "now", "recent", "news",
    "price", "stock", "weather", "score", "live", "update",
    "happening", "right now", "this week", "this month", "2025", "2026"
]


def needs_search(prompt):
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in REALTIME_KEYWORDS)


def search_web(query):
    try:
        result = tavily_client.search(query=query, max_results=3)
        snippets = []
        for r in result.get("results", []):
            snippets.append(f"- {r['title']}: {r['content'][:300]}")
        return "\n".join(snippets)
    except Exception as e:
        return f"(Search failed: {e})"


def query_llm(prompt, model="llama-3.3-70b-versatile"):
    try:
        if needs_search(prompt):
            query = prompt.split("User says:")[-1].replace("ORION response:", "").strip()
            print("🌐 Searching web...")
            search_results = search_web(query)
            prompt = prompt + f"\n\nWeb search results:\n{search_results}\n\nAnswer using the search results above."

        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are ORION, an AI assistant built by Puneeth Gowda. "
                        "You are NOT ChatGPT, NOT You.com, NOT any other AI. "
                        "If asked who made you, say: I was built by Puneeth Gowda. "
                        "Give SHORT answers — 1 to 3 sentences MAX. "
                        "Never add warnings, disclaimers, or extra info nobody asked for. "
                        "Be direct, sharp, and precise. "
                        "For time questions from India, give IST time (UTC+5:30)."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ORION: Error: {str(e)}"