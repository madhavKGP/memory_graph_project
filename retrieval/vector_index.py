import numpy as np
import faiss


class ClaimVectorIndex:

    def __init__(self):

        # Lazy import so Streamlit startup stays fast
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)

        self.claims = []
        self.metadata = []

    # ---------------------------------
    # Add claims to vector index
    # ---------------------------------

    def add_claim(self, subject, relation, obj, evidence):

        text = f"{subject} {relation} {obj}"

        embedding = self.model.encode(text)

        embedding = np.array([embedding]).astype("float32")

        self.index.add(embedding)

        self.claims.append(text)

        self.metadata.append({
            "subject": subject,
            "relation": relation,
            "object": obj,
            "evidence": evidence
        })

    # ---------------------------------
    # Semantic search
    # ---------------------------------

    def search(self, query, top_k=5):

        if len(self.metadata) == 0:
            return []

        embedding = self.model.encode(query)

        embedding = np.array([embedding]).astype("float32")

        distances, indices = self.index.search(embedding, top_k)

        results = []

        for i in indices[0]:

            if i < len(self.metadata):
                results.append(self.metadata[i])

        return results