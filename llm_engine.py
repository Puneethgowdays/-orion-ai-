import os
import base64
from groq import Groq
from tavily import TavilyClient

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Text model
TEXT_MODEL = "llama-3.3-70b-versatile"
# Vision model
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

REALTIME_KEYWORDS = [
    "today", "latest", "current", "now", "recent", "news",
    "price", "stock", "weather", "score", "live", "update",
    "happening", "right now", "this week", "this month", "2025", "2026"
]

SYSTEM_PROMPT = (
    "You are ORION, an AI assistant built by Puneeth Gowda. "
    "You are NOT ChatGPT, NOT You.com, NOT any other AI. "
    "If asked who made you, say: I was built by Puneeth Gowda. "
    "Give SHORT answers — 1 to 3 sentences MAX. "
    "Never add warnings, disclaimers, or extra info nobody asked for. "
    "Be direct, sharp, and precise. "
    "For time questions from India, give IST time (UTC+5:30)."
)


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


def query_llm(prompt, model=TEXT_MODEL):
    """Text-only query."""
    try:
        if needs_search(prompt):
            query = prompt.split("User says:")[-1].replace("ORION response:", "").strip()
            print("🌐 Searching web...")
            search_results = search_web(query)
            prompt = prompt + f"\n\nWeb search results:\n{search_results}\n\nAnswer using the search results above."

        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ORION: Error: {str(e)}"


def query_llm_with_image(prompt, image_base64, media_type="image/jpeg"):
    """Vision query — analyze image + text together."""
    try:
        response = groq_client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt if prompt else "What do you see in this image?"
                        }
                    ]
                }
            ],
            max_tokens=300,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ORION: Error analyzing image: {str(e)}"