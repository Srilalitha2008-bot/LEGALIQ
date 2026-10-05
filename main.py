import pickle

from rag import generate_answer


INDEX_PATH = "data/contract_index.pkl"


print("Loading contract index...")

with open(INDEX_PATH, "rb") as file:
    chunks = pickle.load(file)


print("Contract index loaded successfully.")
print("Total chunks:", len(chunks))


while True:

    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    answer, sources = generate_answer(
        question,
        chunks
    )

    print("\n--- ANSWER ---")
    print(answer)

    print("\n--- SOURCES ---")

    pages = sorted(
        set(source["page"] for source in sources)
    )

    print("Pages:", pages)