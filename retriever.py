import numpy as np
from embeddings import create_embedding


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0

    return np.dot(a, b) / denominator


def retrieve_relevant_chunks(question, chunks, top_k=5):

    question_embedding = create_embedding(question)

    results = []

    for chunk in chunks:

        score = cosine_similarity(
            question_embedding,
            chunk["embedding"]
        )

        results.append({
            "text": chunk["text"],
            "page": chunk["page"],
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]