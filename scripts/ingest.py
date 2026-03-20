import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.tools import setup_index, upsert_documents

def load_knowledge_base(filepath: str) -> list:
    docs = []
    with open(filepath, "r") as f:
        content = f.read().strip()
    blocks = content.split("\n\n")
    for i, block in enumerate(blocks):
        lines = block.strip().split("\n", 1)
        if len(lines) == 2 and lines[0].startswith("title:"):
            title = lines[0].replace("title:", "").strip()
            text = lines[1].strip()
        else:
            title = f"Document {i+1}"
            text = block.strip()
        docs.append({"id": str(i + 1), "title": title, "text": text})
    return docs

if __name__ == "__main__":
    print("Setting up Endee index...")
    setup_index()
    print("Loading knowledge base...")
    docs = load_knowledge_base("data/knowledge_base.txt")
    print(f"Ingesting {len(docs)} documents...")
    upsert_documents(docs)
    print("Done! Knowledge base is ready.")
