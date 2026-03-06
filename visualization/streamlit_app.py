import streamlit as st
import pickle
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

st.set_page_config(layout="wide")

st.title("Grounded Memory Graph Explorer")


# -------------------------
# LOAD GRAPH
# -------------------------

@st.cache_resource
def load_graph():

    with open("memory_graph.pkl", "rb") as f:
        return pickle.load(f)


@st.cache_resource
def load_index():

    with open("vector_index.pkl", "rb") as f:
        return pickle.load(f)


graph = load_graph()
vector_index = load_index()


# -------------------------
# GRAPH VISUALIZATION
# -------------------------

def draw_graph(graph):

    net = Network(height="700px", width="100%", directed=True)

    color_map = {
        "Person": "blue",
        "Organization": "red",
        "Project": "green",
        "Topic": "orange",
        "Concept": "gray"
    }

    for node, data in graph.nodes(data=True):

        node_type = data.get("type", "Concept")

        net.add_node(
            node,
            label=node,
            color=color_map.get(node_type, "gray")
        )

    for u, v, data in graph.edges(data=True):

        net.add_edge(
            u,
            v,
            label=data.get("relation", "")
        )

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")

    net.write_html(temp_file.name)

    HtmlFile = open(temp_file.name, "r", encoding="utf-8")

    components.html(HtmlFile.read(), height=700)


st.subheader("Memory Graph")

draw_graph(graph)


# -------------------------
# SEMANTIC QUERY
# -------------------------

st.sidebar.header("Ask a Question")

query = st.sidebar.text_input("Semantic Search")

if query:

    results = vector_index.search(query)

    st.subheader("Answers")

    for r in results:

        st.write(f"**{r['subject']} → {r['relation']} → {r['object']}**")

        for ev in r["evidence"]:

            st.write(
                f"- {ev['excerpt']}  \n"
                f"source: {ev['source_id']}  \n"
                f"time: {ev['timestamp']}"
            )