import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pickle
from pyvis.network import Network
import tempfile

from dotenv import load_dotenv
load_dotenv()

from groq import Groq


# -----------------------------
# LLM CLIENT
# -----------------------------

def get_llm_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)

client = get_llm_client()


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Email Knowledge Graph",
    layout="wide"
)

st.title("📧 Email Knowledge Graph Explorer")


# -----------------------------
# LOAD MEMORY
# -----------------------------

@st.cache_resource
def load_memory():

    with open("memory_graph.pkl", "rb") as f:
        graph = pickle.load(f)

    with open("vector_index.pkl", "rb") as f:
        vector_index = pickle.load(f)

    return graph, vector_index


graph, vector_index = load_memory()


# -----------------------------
# DFS GRAPH EXPANSION
# -----------------------------

def dfs_expand(graph, start_nodes, depth=2, max_nodes=40):

    visited = set()
    stack = [(node, 0) for node in start_nodes]

    edges = []

    while stack:

        node, level = stack.pop()

        if node in visited or level > depth:
            continue

        visited.add(node)

        if len(visited) > max_nodes:
            break

        for neighbor in graph.successors(node):

            edge_data = graph[node][neighbor]

            edges.append((node, neighbor, edge_data["relation"]))

            stack.append((neighbor, level + 1))

    return visited, edges


# -----------------------------
# GRAPH VISUALIZATION
# -----------------------------

def draw_graph(nodes, edges):

    net = Network(
        height="600px",
        width="100%",
        directed=True,
        bgcolor="#0E1117",
        font_color="white"
    )

    net.barnes_hut()

    for n in nodes:

        net.add_node(
            n,
            label=n,
            color="#4F8EF7",
            size=15
        )

    for u, v, relation in edges:

        if u not in net.get_nodes():
            net.add_node(u)

        if v not in net.get_nodes():
            net.add_node(v)

        net.add_edge(
            u,
            v,
            label=relation,
            color="#AAAAAA"
        )

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")

    net.save_graph(temp_file.name)

    html = open(temp_file.name).read()

    st.components.v1.html(html, height=600)


# -----------------------------
# LLM REASONING
# -----------------------------

def run_reasoning(query, claims):

    context = ""

    for c in claims:
        context += f"{c['subject']} -- {c['relation']} --> {c['object']}\n"

    prompt = f"""
You are analyzing an email knowledge graph.

User Question:
{query}

Facts:
{context}

Return the answer in this format:

Confirmed relationships:
• Person ↔ Person

Possible relationships:
• Person ↔ Person

Evidence:
• Short quote

Only use the provided facts.
Be concise.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# QUERY INPUT
# -----------------------------

query = st.text_input(
    "Ask a question about the email network",
    placeholder="Example: who met whom"
)

if query:

    results = vector_index.search(query, top_k=5)

    col1, col2 = st.columns([1,1])

    # -------------------------
    # SEMANTIC RESULTS
    # -------------------------

    with col1:

        st.subheader("🔎 Semantic Retrieval")

        for r in results:

            st.markdown(
                f"**{r['subject']}** → `{r['relation']}` → **{r['object']}**"
            )

            for ev in r["evidence"]:
                st.caption(ev.get("excerpt",""))


    # -------------------------
    # GRAPH
    # -------------------------

    with col2:

        st.subheader("🕸 Graph")

        seed_nodes = set()

        for r in results:
            seed_nodes.add(r["subject"])
            seed_nodes.add(r["object"])

        nodes, edges = dfs_expand(graph, seed_nodes)

        draw_graph(nodes, edges)


    # -------------------------
    # LLM REASONING
    # -------------------------

    st.divider()

    st.subheader("🧠 AI Reasoning")

    with st.spinner("Analyzing relationships..."):

        explanation = run_reasoning(query, results)

    st.markdown(explanation)