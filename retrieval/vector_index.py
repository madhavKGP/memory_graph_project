from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


class ClaimVectorIndex:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)

        self.claims = []
        self.metadata = []

    def add_claim(self, subject, relation, obj, evidence):

        text = f"{subject} {relation} {obj}"

        embedding = self.model.encode([text])[0]

        self.index.add(np.array([embedding]).astype("float32"))

        self.claims.append(text)

        self.metadata.append({
            "subject": subject,
            "relation": relation,
            "object": obj,
            "evidence": evidence
        })

    def search(self, query, k=5):

        embedding = self.model.encode([query])[0]

        distances, indices = self.index.search(
            np.array([embedding]).astype("float32"), k
        )

        results = []

        for i in indices[0]:

            if i < len(self.metadata):
                results.append(self.metadata[i])

        return results