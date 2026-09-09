"""Chat interface and citation display rendering."""

import streamlit as st

from app.rag.pipeline import RAGPipeline
from app.ui.components import render_button


def render_chat_page() -> None:
    """Render the document question-answering interface."""

    st.title("Ask DocuMind")
    st.write(
        "Ask questions about your uploaded documents. "
        "Answers are generated from retrieved document context."
    )

    question = st.text_input(
        "Question",
        placeholder="What does the document say about...?",
    )

    if render_button(
        "Ask",
        variant="primary",
        key="ask",
    ):
        try:
            pipeline = RAGPipeline()

            with st.spinner("Searching your documents..."):
                result = pipeline.query(question)

            st.subheader("Answer")
            st.write(result.answer)

            if result.documents:
                st.subheader("Sources")

                for index, document in enumerate(
                    result.documents,
                    start=1,
                ):
                    source = document.metadata.get(
                        "source",
                        "Unknown document",
                    )
                    page = document.metadata.get("page")

                    if page is not None:
                        page_display = int(page) + 1
                        st.caption(
                            f"{index}. {source} • Page {page_display}"
                        )
                    else:
                        st.caption(f"{index}. {source}")

            else:
                st.info(
                    "No supporting documents were retrieved for this question."
                )

        except ValueError as error:
            st.error(str(error))
        except OSError as error:
            st.error(
                f"Unable to access the document store: {error}"
            )