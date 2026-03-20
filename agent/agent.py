import os
import json
from groq import Groq
from dotenv import load_dotenv
from agent.tools import search_knowledge

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MAX_ITERATIONS = 3

SYSTEM_PROMPT = """You are a smart research agent with access to a knowledge base.

At each step, respond ONLY with a JSON object. Two options:

1. Search for more context:
{"action": "search", "query": "what to search for"}

2. Give final answer:
{"action": "answer", "response": "your final answer here"}

Always search at least once before answering."""

def run_agent(user_question: str) -> str:
    print(f"\n[Agent] Question: {user_question}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]

    for iteration in range(MAX_ITERATIONS):
        print(f"[Agent] Thinking... (step {iteration + 1})")

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            decision = json.loads(raw)
        except json.JSONDecodeError:
            return raw

        action = decision.get("action")

        if action == "answer":
            print("[Agent] Has enough context — answering!")
            return decision.get("response", "No answer generated.")

        elif action == "search":
            query = decision.get("query", user_question)
            print(f"[Agent] Searching Endee for: '{query}'")

            results = search_knowledge(query, top_k=3)
            context = "\n\n".join(
                f"[{r['title']}] score:{r['score']}\n{r['text']}"
                for r in results
            ) if results else "No results found."

            print(f"[Agent] Got {len(results)} results from Endee.")

            messages.append({"role": "assistant", "content": raw})
            messages.append({
                "role": "user",
                "content": f"Search results:\n\n{context}\n\nNow decide: search again OR give final answer as JSON."
            })

    messages.append({
        "role": "user",
        "content": "You have hit the search limit. Give your best final answer now."
    })
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content.strip()