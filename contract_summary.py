import ollama

from retriever import retrieve_relevant_chunks


LLM_MODEL = "llama3.2"


def generate_contract_summary(chunks):

    question = """
Provide a concise summary of this legal contract.

Focus on:

1. Purpose of the contract
2. Contract duration and extension
3. Termination conditions
4. Payment and financial terms
5. Security deposit
6. Important obligations
7. Penalties or fines
8. Dispute resolution
9. Governing law and jurisdiction
10. Other important terms
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
an uploaded contract.

STRICT RULES:

1. Use ONLY the provided contract context.
2. Do NOT use outside knowledge.
3. Do NOT guess, assume, or infer missing information.
4. Do NOT invent clause numbers, section numbers, dates,
   amounts, percentages, durations, names, or conditions.
5. For every important fact in the summary, mention the
   PDF page that directly supports it.
6. If an item is not explicitly supported by the context,
   write:
   "Not specified in the retrieved contract context."
7. Do NOT confuse similar terms. For example, an extension
   of performance due to force majeure is NOT the same as
   extension or renewal of the contract.
8. For monetary amounts, dates, percentages, and durations,
   reproduce the value exactly as stated in the context.
9. Do not combine information from unrelated clauses to
   create a new condition.
10. Do not provide legal advice or give a legal conclusion.
    Only summarize what the contract states.

CONTRACT CONTEXT:
{context}

Prepare a concise summary using these headings:

1. Purpose of Contract
2. Contract Duration and Extension
3. Termination
4. Payment and Financial Terms
5. Security Deposit
6. Important Obligations
7. Penalties or Fines
8. Dispute Resolution
9. Governing Law and Jurisdiction
10. Other Important Terms

SUMMARY:
"""

    response = ollama.generate(
        model=LLM_MODEL,
        prompt=prompt
    )

    return response["response"], relevant_chunks