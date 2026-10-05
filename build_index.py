import pickle

from pdf_reader import extract_text_from_pdf
from chunker import create_chunks
from embeddings import create_embedding


PDF_PATH = "data/contract.pdf"
INDEX_PATH = "data/contract_index.pkl"


print("Reading contract...")

pages = extract_text_from_pdf(PDF_PATH)

print("Total pages:", len(pages))


print("Creating chunks...")

chunks = create_chunks(pages)

print("Total chunks:", len(chunks))


print("Creating embeddings...")

for i, chunk in enumerate(chunks):

    chunk["embedding"] = create_embedding(
        chunk["text"]
    )

    print(f"Embedded {i + 1}/{len(chunks)}")


with open(INDEX_PATH, "wb") as file:
    pickle.dump(chunks, file)


print("\nIndex created successfully.")
print("Saved to:", INDEX_PATH)