from groq import Groq
from tavily import TavilyClient
import json

# 🔑 API Keys
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "gsk_xxxx...")

# Keywords that trigger a web search
REALTIME_KEYWORDS = [
    "today", "latest", "current", "now", "recent", "news",
    "price", "stock", "weather", "score", "live", "update",
    "happening", "right now", "this week", "this month", "2024", "2025", "2026"
]


def needs_search(prompt):
    """Check if the prompt needs real-time web data."""
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in REALTIME_KEYWORDS)


def search_web(query):
    """Search the web using Tavily and return a summary."""
    try:
        result = tavily_client.search(query=query, max_results=3)
        snippets = []
        for r in result.get("results", []):
            snippets.append(f"- {r['title']}: {r['content'][:300]}")
        return "\n".join(snippets)
    except Exception as e:
        return f"(Search failed: {e})"


def query_llm(prompt, model="llama-3.3-70b-versatile"):
    """
    Query Groq API. Automatically searches web for real-time questions.
    """
    try:
        # ✅ Check if web search is needed
        if needs_search(prompt):
            # Extract the last user message as search query
            query = prompt.split("User says:")[-1].replace("ORION response:", "").strip()
            print("🌐 Searching web...")
            search_results = search_web(query)
            # Inject search results into prompt
            prompt = prompt + f"\n\nReal-time web search results:\n{search_results}\n\nUse the above search results to answer accurately."

        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ORION: Error: {str(e)}"