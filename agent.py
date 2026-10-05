import pickle

from rag import generate_answer
from clause_extractor import extract_clauses
from contract_summary import generate_contract_summary
from risk_analysis import analyze_contract_risks


INDEX_PATH = "data/contract_index.pkl"


def load_contract():

    with open(INDEX_PATH, "rb") as file:
        chunks = pickle.load(file)

    return chunks


def ask_question(chunks):

    question = input("\nEnter your question: ")

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


def show_summary(chunks):

    print("\nGenerating contract summary...")

    summary, sources = generate_contract_summary(
        chunks
    )

    print("\n--- CONTRACT SUMMARY ---")
    print(summary)

    print("\n--- SOURCES ---")

    pages = sorted(
        set(source["page"] for source in sources)
    )

    print("Pages:", pages)


def show_clauses(chunks):

    print("\nExtracting key clauses...")

    results = extract_clauses(chunks)

    print("\n--- KEY CONTRACT CLAUSES ---")

    for clause, information in results.items():

        print(f"\n### {clause} ###")
        print(information)


def show_risks(chunks):

    print("\nAnalyzing risks and attention points...")

    analysis, sources = analyze_contract_risks(
        chunks
    )

    print("\n--- RISK / ATTENTION ANALYSIS ---")
    print(analysis)

    print("\n--- SOURCES ---")

    pages = sorted(
        set(source["page"] for source in sources)
    )

    print("Pages:", pages)


def main():

    print("Loading contract index...")

    chunks = load_contract()

    print("Contract index loaded successfully.")
    print("Total chunks:", len(chunks))

    while True:

        print("\n")
        print("========================================")
        print("       LEGAL CONTRACT AI AGENT")
        print("========================================")
        print("1. Ask a Question")
        print("2. Contract Summary")
        print("3. Extract Key Clauses")
        print("4. Risk / Attention Analysis")
        print("5. Exit")
        print("========================================")

        choice = input("Choose an option: ")

        if choice == "1":

            ask_question(chunks)

        elif choice == "2":

            show_summary(chunks)

        elif choice == "3":

            show_clauses(chunks)

        elif choice == "4":

            show_risks(chunks)

        elif choice == "5":

            print("\nExiting Legal Contract AI Agent...")
            break

        else:

            print("\nInvalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()