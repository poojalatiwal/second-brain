from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/e5-large-v2"

print("📌 Loading embedding model:", MODEL_NAME)
model = SentenceTransformer(MODEL_NAME)

EMBEDDING_DIM = model.get_sentence_embedding_dimension()
print("✅ Embedding dimension:", EMBEDDING_DIM)

def get_embedding(text: str) -> list[float]:
    return model.encode(
        text,
        normalize_embeddings=True
    ).tolist()
