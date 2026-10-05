import ollama

from pdf_reader import extract_text_from_pdf
from chunker import create_chunks
from embeddings import create_embedding
from retriever import retrieve_relevant_chunks


LLM_MODEL = "llama3.2"


def prepare_document(pdf_path):

    pages = extract_text_from_pdf(pdf_path)

    chunks = create_chunks(pages)

    for chunk in chunks:
        chunk["embedding"] = create_embedding(
            chunk["text"]
        )

    return chunks


def generate_answer(question, chunks):

    relevant_chunks = retrieve_relevant_chunks(
        question,
        chunks,
        top_k=5
    )

    context = ""

    for chunk in relevant_chunks:

        context += (
            f"\n[PDF Page {chunk['page']}]\n"
            f"{chunk['text']}\n"
        )

    prompt =  f"""
You are a Legal Contract Assistant helping a lawyer review
an uploaded contract.

STRICT RULES:

1. Answer ONLY using the provided contract context.
2. Do NOT use outside knowledge.
3. Do NOT guess, assume, or infer missing facts.
4. Do NOT invent clause numbers, section numbers, dates,
   amounts, percentages, durations, or names.
5. If a requested fact is not explicitly supported by the
   provided context, say:
   "I could not find that information in the uploaded document."
6. If the question has multiple parts, answer EVERY part
   separately.
7. Mention a PDF page ONLY when that page supports the
   statement being made.
8. If the context contains conflicting information, clearly
   state that the retrieved context appears inconsistent
   instead of choosing one value yourself.
9. For monetary amounts, dates, percentages, and contract
   durations, reproduce the value exactly as stated in the
   context.
10. Do not provide legal advice or make a legal conclusion.
    Only report what the contract states.

CONTRACT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = ollama.generate(
        model=LLM_MODEL,
        prompt=prompt
    )

    return response["response"], relevant_chunks