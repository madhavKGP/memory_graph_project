# Email Knowledge Graph Explorer

An AI system that converts raw emails into a **structured knowledge graph**, enables **semantic search over relationships**, and performs **LLM-powered reasoning** on the extracted information.

This project demonstrates how **unstructured communication data (emails)** can be transformed into a **queryable knowledge network**.

Repository: https://github.com/madhavKGP/memory_graph_project

---

# Project Overview

The system processes raw emails and builds a knowledge graph that supports **semantic retrieval and reasoning**.

## Pipeline

```
Emails
↓
LLM Information Extraction
↓
Entity + Relation Normalization
↓
Knowledge Graph Construction (NetworkX)
↓
Vector Embedding Index (FAISS)
↓
Semantic Retrieval + Graph Traversal (DFS)
↓
LLM Reasoning
↓
Interactive Graph UI (Streamlit)
```

The system allows users to ask questions such as:

- Who met whom?
- Who works with Phillip Allen?
- Which meetings were scheduled?

And receive:

- Semantic search results
- Interactive graph exploration
- LLM-generated reasoning over the graph

---

# Example Interface

The Streamlit UI provides three core capabilities.

### Semantic Retrieval
Top relevant relationships retrieved using vector embeddings.

### Interactive Graph
Drag-and-drop visualization of relationships extracted from emails.

### AI Reasoning
LLM-generated explanations derived from graph relationships.

---

# Dataset

This project uses the **Enron Email Dataset**.

Download it using:

```python
import kagglehub

path = kagglehub.dataset_download("wcukierski/enron-email-dataset")

print("Path to dataset files:", path)
```

Required file:

```
emails.csv
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/madhavKGP/memory_graph_project.git
cd memory_graph_project
```

## Create a Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```
networkx==3.3
streamlit==1.36.0
pyvis==0.3.2
faiss-cpu==1.8.0
sentence-transformers==3.0.1
numpy==1.26.4
python-dotenv==1.0.1
groq==0.9.0
kagglehub==0.3.3
pandas==2.2.2
tqdm==4.66.4
```

---

# Environment Variables

Create a `.env` file in the root directory.

```
GROQ_API_KEY=your_api_key_here
```

This key is used for **LLM reasoning via the Groq API**.

---

# Running the Project

## 1. Test the Pipeline (5 Emails)

Runs the full pipeline on a small sample.

```bash
python main.py
```

This verifies:

- extraction
- graph construction
- retrieval
- reasoning

---

## 2. Build Memory Graph (100 Emails)

To build the knowledge graph and vector index:

```bash
python build_memory.py
```

This creates:

```
memory_graph.pkl
vector_index.pkl
```

These files store:

- the knowledge graph
- the semantic vector index

---

## 3. Run the UI

Launch the interactive interface:

```bash
streamlit run visualization/streamlit_app.py
```


# Project Structure

```
memory_graph_project
│
├── data
│   ├── loader.py
│   └── email_parser.py
│
├── extraction
│   ├── extractor.py
│   └── prompt.py
│
├── dedup
│   ├── entity_normalizer.py
│   ├── entity_resolution.py
│   └── relation_normalizer.py
│
├── graph
│   └── graph_builder.py
│
├── retrieval
│   ├── vector_index.py
│   ├── retriever.py
│   ├── graph_reasoning.py
│   └── answer_formatter.py
│
├── visualization
│   └── streamlit_app.py
│
├── models
│   ├── email_artifact.py
│   └── extraction_schema.py
│
├── build_memory.py
├── main.py
├── requirements.txt
└── README.md
```

---

# File Responsibilities

## data/

Handles **email loading and parsing**.

## extraction/

Uses LLM prompting to extract:

- entities
- claims
- relationships

## dedup/

Normalizes extracted information.

Includes:

- entity normalization
- entity resolution
- relation normalization

## graph/

Constructs the knowledge graph using **NetworkX**.

Responsibilities:

- node creation
- edge creation
- evidence tracking
- deduplication

## retrieval/

Implements the retrieval system.

### vector_index.py

Embedding-based semantic search using:

- SentenceTransformers
- FAISS

### retriever.py

Keyword-based graph retrieval.

### graph_reasoning.py

DFS graph traversal to expand relationship context.

## visualization/

Provides the **Streamlit interface**.

Features:

- semantic search
- interactive graph visualization
- LLM reasoning

---

# Thought Process

The main design goal was to build a **GraphRAG-style architecture**.

Instead of searching raw documents, the system:

1. Extracts structured knowledge
2. Stores it as a knowledge graph
3. Performs semantic retrieval on relationships
4. Expands context using graph traversal
5. Uses an LLM to reason over graph facts

This enables **relationship-level reasoning**, which traditional RAG systems struggle to achieve.

---

# Key Challenges

## 1. Noisy LLM Outputs

LLM extraction sometimes produced:

- malformed JSON
- incomplete claims
- missing objects

Solution:

- parsing validation
- skipping invalid claims

---

## 2. Entity Duplication

Examples:

```
Phillip Allen
Phillip K Allen
Phillip K. Allen
```

Solution:

**Entity normalization and canonicalization.**

---

## 3. Relation Variability

Examples:

```
sent email to
sent_email_to
sent mail to
```

Solution:

Convert relations into **snake_case** format.

---

## 4. Graph Explosion

Emails generate many nodes quickly.

Solution:

- DFS depth limits
- graph expansion constraints

---

## 5. Retrieval Quality

Keyword search alone was insufficient.

Solution:

Vector embeddings using:

```
sentence-transformers/all-MiniLM-L6-v2
```

with **FAISS indexing**.

---

# Technologies Used

- Python
- NetworkX
- SentenceTransformers
- FAISS
- Streamlit
- Groq LLM API

---

# Future Improvements

Possible improvements include:

- Neo4j graph database integration
- graph embeddings
- multi-hop reasoning
- graph highlight visualization
- graph summarization

---

# Conclusion

This project demonstrates how **LLMs + Knowledge Graphs + Vector Search** can be combined to create a **GraphRAG system** for structured reasoning over communication data.

The system can:

- extract structured knowledge from emails
- explore relationships visually
- answer complex questions about interactions

---

# License

MIT License