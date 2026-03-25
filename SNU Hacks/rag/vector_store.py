import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle
class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.index_path = "rag/faiss.index"
        self.text_path = "rag/texts.pkl"

        # Load existing memory if available
        if os.path.exists(self.index_path) and os.path.exists(self.text_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.text_path, "rb") as f:
                self.texts = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(384)
            self.texts = []


    def add(self, text):
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding))
        self.texts.append(text)
        self.save()

    def search(self, query, k=3):
        if len(self.texts) == 0:
            return []
        query_embedding = self.model.encode([query])
        D, I = self.index.search(np.array(query_embedding), k)
        return [self.texts[i] for i in I[0]]

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.text_path, "wb") as f:
            pickle.dump(self.texts, f)

    def load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        if os.path.exists(self.text_path):
            with open(self.text_path, "rb") as f:
                self.texts = pickle.load(f)