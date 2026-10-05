import os
import sys
import hashlib
import streamlit as st

# =========================================================
# PROJECT PATH
# =========================================================

SRC_PATH = os.path.join(
    os.path.dirname(__file__),
    "src"
)

sys.path.insert(0, SRC_PATH)


# =========================================================
# IMPORT BACKEND
# =========================================================

from pdf_reader import extract_text_from_pdf
from chunker import create_chunks
from embeddings import create_embedding

from rag import generate_answer
from clause_extractor import extract_clauses
from contract_summary import generate_contract_summary
from risk_analysis import analyze_contract_risks


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="LegalIQ",
    page_icon="⚖️",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "pages" not in st.session_state:
    st.session_state.pages = None

if "file_id" not in st.session_state:
    st.session_state.file_id = None

if "active_feature" not in st.session_state:
    st.session_state.active_feature = None

if "clause_results" not in st.session_state:
    st.session_state.clause_results = None

if "summary_result" not in st.session_state:
    st.session_state.summary_result = None

if "risk_result" not in st.session_state:
    st.session_state.risk_result = None


# =========================================================
# HEADER
# =========================================================

st.title("⚖️ LEGALIQ")

st.caption(
    "AI-Powered Legal Contract Intelligence"
)

st.divider()


# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns(
    [1, 2.5],
    gap="large"
)


# =========================================================
# LEFT SIDE — DOCUMENT
# =========================================================

with left:

    st.subheader("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload a legal contract",
        type=["pdf"]
    )


    # -----------------------------------------------------
    # PROCESS PDF
    # -----------------------------------------------------

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        current_file_id = hashlib.md5(
            file_bytes
        ).hexdigest()


        # Process only if this is a new file
        if current_file_id != st.session_state.file_id:

            os.makedirs(
                "data",
                exist_ok=True
            )

            upload_path = os.path.join(
                "data",
                "uploaded_contract.pdf"
            )


            with open(
                upload_path,
                "wb"
            ) as file:

                file.write(file_bytes)


            # Clear previous results
            st.session_state.clause_results = None
            st.session_state.summary_result = None
            st.session_state.risk_result = None
            st.session_state.active_feature = None


            with st.spinner(
                "Processing contract..."
            ):

                pages = extract_text_from_pdf(
                    upload_path
                )

                chunks = create_chunks(
                    pages
                )


                for chunk in chunks:

                    chunk["embedding"] = create_embedding(
                        chunk["text"]
                    )


            st.session_state.file_id = current_file_id
            st.session_state.pages = pages
            st.session_state.chunks = chunks


            st.success(
                "Contract processed successfully."
            )


    # -----------------------------------------------------
    # SIMPLE DOCUMENT INFORMATION
    # -----------------------------------------------------

    if st.session_state.chunks is not None:

        st.write(
            f"**File:** {uploaded_file.name}"
        )

        st.write(
            f"**Pages:** {len(st.session_state.pages)}"
        )

        st.write(
            f"**Chunks:** {len(st.session_state.chunks)}"
        )

        st.write(
            "**AI:** Llama 3.2"
        )

        st.write(
            "**Mode:** Local RAG"
        )


# =========================================================
# RIGHT SIDE
# =========================================================

with right:

    st.subheader(
        "What would you like to do?"
    )

    st.caption(
        "Choose an operation to analyze your contract."
    )


    # =====================================================
    # FOUR OPTIONS
    # =====================================================

    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "💬 Ask Contract",
            use_container_width=True
        ):

            st.session_state.active_feature = "ask"


        if st.button(
            "📋 Contract Summary",
            use_container_width=True
        ):

            st.session_state.active_feature = "summary"


    with col2:

        if st.button(
            "📑 Key Clauses",
            use_container_width=True
        ):

            st.session_state.active_feature = "clauses"


        if st.button(
            "⚠️ Attention Points",
            use_container_width=True
        ):

            st.session_state.active_feature = "risk"


    st.divider()


    # =====================================================
    # IF NO FILE
    # =====================================================

    if (
        st.session_state.active_feature is not None
        and st.session_state.chunks is None
    ):

        st.warning(
            "Please upload a PDF contract first."
        )


    # =====================================================
    # ASK CONTRACT
    # =====================================================

    if (
        st.session_state.active_feature == "ask"
        and st.session_state.chunks is not None
    ):

        st.subheader(
            "💬 Ask About Contract"
        )

        question = st.text_area(
            "Enter your question",
            placeholder=(
                "Example: What are the termination "
                "conditions of the contract?"
            )
        )


        if st.button(
            "🔎 Ask Legal Agent",
            use_container_width=True
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "Analyzing contract..."
                ):

                    answer, sources = generate_answer(
                        question,
                        st.session_state.chunks
                    )


                st.subheader("Answer")

                st.write(answer)


                st.subheader("📚 Evidence")

                pages = sorted(
                    set(
                        source["page"]
                        for source in sources
                    )
                )

                st.write(
                    "Pages:",
                    ", ".join(
                        str(page)
                        for page in pages
                    )
                )


                with st.expander(
                    "View retrieved contract text"
                ):

                    for source in sources:

                        st.write(
                            f"**Page {source['page']}**"
                        )

                        st.write(
                            source["text"]
                        )

                        st.divider()


    # =====================================================
    # KEY CLAUSES
    # =====================================================

    elif (
        st.session_state.active_feature == "clauses"
        and st.session_state.chunks is not None
    ):

        st.subheader(
            "📑 Key Contract Clauses"
        )

        st.write(
            "Extract important clauses from the contract."
        )


        if st.session_state.clause_results is None:

            if st.button(
                "🔎 Extract Key Clauses",
                use_container_width=True
            ):

                with st.spinner(
                    "Extracting key clauses..."
                ):

                    results = extract_clauses(
                        st.session_state.chunks
                    )

                st.session_state.clause_results = results

                st.rerun()


        else:

            for clause, information in (
                st.session_state.clause_results.items()
            ):

                with st.expander(
                    clause
                ):

                    st.write(
                        information
                    )


    # =====================================================
    # CONTRACT SUMMARY
    # =====================================================

    elif (
        st.session_state.active_feature == "summary"
        and st.session_state.chunks is not None
    ):

        st.subheader(
            "📋 Contract Summary"
        )

        st.write(
            "Generate a concise summary of the contract."
        )


        if st.session_state.summary_result is None:

            if st.button(
                "📋 Generate Summary",
                use_container_width=True
            ):

                with st.spinner(
                    "Generating summary..."
                ):

                    summary, sources = (
                        generate_contract_summary(
                            st.session_state.chunks
                        )
                    )

                st.session_state.summary_result = (
                    summary,
                    sources
                )

                st.rerun()


        else:

            summary, sources = (
                st.session_state.summary_result
            )

            st.write(summary)


            pages = sorted(
                set(
                    source["page"]
                    for source in sources
                )
            )

            st.write(
                "Source pages:",
                ", ".join(
                    str(page)
                    for page in pages
                )
            )


    # =====================================================
    # ATTENTION POINTS
    # =====================================================

    elif (
        st.session_state.active_feature == "risk"
        and st.session_state.chunks is not None
    ):

        st.subheader(
            "⚠️ Attention Points"
        )

        st.write(
            "Identify areas of the contract that may "
            "require closer review."
        )


        if st.session_state.risk_result is None:

            if st.button(
                "⚠️ Analyze Attention Points",
                use_container_width=True
            ):

                with st.spinner(
                    "Analyzing contract..."
                ):

                    analysis, sources = (
                        analyze_contract_risks(
                            st.session_state.chunks
                        )
                    )

                st.session_state.risk_result = (
                    analysis,
                    sources
                )

                st.rerun()


        else:

            analysis, sources = (
                st.session_state.risk_result
            )

            st.write(analysis)


            pages = sorted(
                set(
                    source["page"]
                    for source in sources
                )
            )

            st.write(
                "Source pages:",
                ", ".join(
                    str(page)
                    for page in pages
                )
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "LegalIQ • Llama 3.2 • nomic-embed-text • Local RAG"
)
