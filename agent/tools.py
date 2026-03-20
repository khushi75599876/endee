from endee import Endee, Precision
from agent.embedder import embed

INDEX_NAME = "knowledge_base"
DIMENSION = 384

client = Endee()

def setup_index():
    try:
        client.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            space_type="cosine",
            precision=Precision.INT8
        )
        print("[Endee] Index created.")
    except Exception:
        print("[Endee] Index already exists.")

def upsert_documents(docs: list):
    index = client.get_index(name=INDEX_NAME)
    vectors = []
    for doc in docs:
        vectors.append({
            "id": doc["id"],
            "vector": embed(doc["text"]),
            "meta": {"title": doc["title"], "text": doc["text"]}
        })
    index.upsert(vectors)
    print(f"[Endee] Uploaded {len(vectors)} documents.")

def search_knowledge(query: str, top_k: int = 3) -> list:
    index = client.get_index(name=INDEX_NAME)
    query_vector = embed(query)
    results = index.query(vector=query_vector, top_k=top_k)
    retrieved = []
    for r in results:
        retrieved.append({
            "title":r["meta"].get("title", "Unknown"),
            "text": r["meta"].get("text", ""),
            "score": round(r["similarity"], 3)
        })
    return retrieved