import ollama

from retriever import retrieve_relevant_chunks


LLM_MODEL = "llama3.2"


def analyze_contract_risks(chunks):

    question = """
Analyze the contract for important risk and attention points
that a lawyer should review.

Focus on:

1. Termination rights and notice periods
2. Financial obligations, deposits, payments and fines
3. Unusual or strict obligations on either party
4. Liability and indemnification
5. Dispute resolution and jurisdiction
6. Force majeure provisions
7. Contract duration and extension
8. Missing or unclear important terms

For every point:

- Describe what the contract actually states.
- Mention the relevant PDF page.
- Do NOT assume that something is a legal risk merely because
  it is unusual.
- Do NOT provide legal advice.
- Do NOT invent missing information.

If an important area is not found in the retrieved context,
say "Not clearly specified in the retrieved contract context."
"""

    relevant_chunks = retrieve_relevant_chunks(
        question,
        chunks,
        top_k=10
    )

    context = ""

    for chunk in relevant_chunks:

        context += (
            f"\n[PDF Page {chunk['page']}]\n"
            f"{chunk['text']}\n"
        )

    prompt = f"""
You are a Legal Contract Assistant helping a lawyer review
a contract.

{question}

CONTRACT CONTEXT:
{context}

RISK / ATTENTION ANALYSIS:
"""

    response = ollama.generate(
        model=LLM_MODEL,
        prompt=prompt
    )

    return response["response"], relevant_chunks