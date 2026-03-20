# AI Knowledge Agent powered by Endee

## Problem Statement
Building an AI agent that autonomously retrieves knowledge from a vector database to answer questions — demonstrating agentic AI with Endee as the core memory and retrieval layer.

## System Design
User Question → Embed Query → Search Endee → LLM Decision → Search Again? → Final Answer

## How Endee is Used
- Stores embedded document chunks in a cosine-similarity index (384 dimensions)
- Acts as the agent's long-term memory and knowledge retrieval tool
- The agent queries Endee iteratively (up to 3 times) until it has enough context
- Uses Endee's Python SDK to upsert vectors and run similarity queries

## Tech Stack
- **Endee** — Vector database (core of the project)
- **Python** — Main programming language
- **sentence-transformers** — Free local embeddings (all-MiniLM-L6-v2)
- **Groq + LLaMA 3.1** — Free LLM for agent reasoning
- **Docker** — Runs Endee server locally

## Project Structure
```
ai-knowledge-agent/
├── agent/
│   ├── __init__.py
│   ├── embedder.py       # Converts text to vectors
│   ├── tools.py          # Endee search tool
│   └── agent.py          # Agentic loop brain
├── data/
│   └── knowledge_base.txt
├── scripts/
│   └── ingest.py         # Loads docs into Endee
├── main.py               # Run this to chat
└── README.md
```

## Setup Instructions

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/endee.git
cd endee/ai-knowledge-agent
```

### 2. Start Endee with Docker
```bash
docker run -d -p 8080:8080 --name endee-server endeeio/endee-server:latest
```

### 3. Install dependencies
```bash
pip install endee sentence-transformers groq python-dotenv
```

### 4. Add your API key
Create a `.env` file and add your Groq API key from https://console.groq.com
```
GROQ_API_KEY=your_groq_key_here
```

### 5. Load knowledge base into Endee
```bash
python scripts/ingest.py
```

### 6. Run the agent
```bash
python main.py
```

## Example Output
```
You: What is Endee and how does it work?

[Agent] Thinking... (step 1)
[Agent] Searching Endee for: 'Endee definition and functionality'
[Agent] Got 3 results from Endee.
[Agent] Thinking... (step 2)
[Agent] Searching Endee for: 'relation between Endee and Agentic AI'
[Agent] Got 3 results from Endee.

Agent: Endee is a high-performance open-source vector database that can
handle up to 1 billion vectors on a single node...
```

## Mandatory Steps Completed
- Starred the official Endee repository
- Forked the repository to personal GitHub account
- Built project using the forked version as base