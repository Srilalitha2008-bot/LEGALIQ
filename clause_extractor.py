import ollama

from retriever import retrieve_relevant_chunks


LLM_MODEL = "llama3.2"


CLAUSES = [
    "Contract Duration",
    "Termination",
    "Payment",
    "Security Deposit",
    "Confidentiality",
    "Liability",
    "Indemnification",
    "Dispute Resolution",
    "Governing Law",
    "Penalties",
    "Renewal"
]


def extract_clauses(chunks):

    results = {}

    for clause in CLAUSES:

        relevant_chunks = retrieve_relevant_chunks(
            clause,
            chunks,
            top_k=5
        )

        context = ""

        for chunk in relevant_chunks:

            context += (
                f"\n[PDF Page {chunk['page']}]\n"
                f"{chunk['text']}\n"
            )

        prompt = f"""
You are a Legal Contract Assistant.

Extract the information about the following
contract clause:

CLAUSE:
{clause}

Use ONLY the provided contract context.

Do not use outside knowledge.
Do not invent information.

If the clause is not clearly found in the
provided context, say:

"Not clearly specified in the retrieved contract context."

Mention the PDF page when possible.

CONTRACT CONTEXT:
{context}

CLAUSE INFORMATION:
"""

        response = ollama.generate(
            model=LLM_MODEL,
            prompt=prompt
        )

        results[clause] = response["response"]

    return results