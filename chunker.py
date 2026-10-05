def create_chunks(pages, chunk_size=1200, overlap=200):

    chunks = []

    for page in pages:
        text = page["text"].strip()
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "page": page["page"]
                })

            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":

    from pdf_reader import extract_text_from_pdf

    pages = extract_text_from_pdf("data/contract.pdf")

    chunks = create_chunks(pages)

    print("Total pages:", len(pages))
    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i + 1} ---")
        print("Page:", chunk["page"])
        print(chunk["text"][:500])