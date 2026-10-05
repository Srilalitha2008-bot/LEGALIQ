import ollama

EMBED_MODEL = "nomic-embed-text"


def create_embedding(text):

    response = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )

    return response["embedding"]


if __name__ == "__main__":

    vector = create_embedding(
        "What is the termination period?"
    )

    print("Embedding created successfully.")
    print("Embedding length:", len(vector))