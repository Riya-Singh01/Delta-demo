import streamlit as st
import PyPDF2
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


def extract_text_from_pdf():
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
            st.session_state.uploaded_pdf_text = text
            st.success("PDF uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")


def model_llm():
    return ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    groq_api_key="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"
)


def query_pdf_content(query):
    if "uploaded_pdf_text" not in st.session_state or not st.session_state.uploaded_pdf_text:
        st.warning("Please upload a PDF before asking questions!")
        return

    prompt = PromptTemplate.from_template(
        """
        You are a PDF content assistant. The following text is extracted from a PDF document:
        ---
        {pdf_content}
        ---
        Answer the user's query based on the above content. If the answer is not found, reply with 'No information exists.'
        Query: {query}
        """
    )
    llm = model_llm()
    chain = prompt | llm
    response = chain.invoke({"pdf_content": st.session_state.uploaded_pdf_text, "query": query})
    return response.content.strip()


def handle_query(query):
    if "active_conversation" not in st.session_state or not st.session_state.active_conversation:
        st.warning("Start a new conversation before asking questions!")
        return

    response = query_pdf_content(query)
    if response:
        st.session_state.conversations[st.session_state.active_conversation]["messages"].append(
            {"query": query, "response": response})
        st.write(f"**Bot:** {response}")



def chat_ui():
    st.markdown("""
    <style>
    .genome-logo {
        font-size: 32px;
        font-weight: bold;
        color: #00FF00;
        background: linear-gradient(to right, #00FF00, #0099FF);
        -webkit-background-clip: text;
        color: transparent;
        text-align: center;
    }
    </style>
    <div class="genome-logo">Genome.AI</div>
    """, unsafe_allow_html=True)

    st.title("PDF Query Chatbot")

    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
    if "active_conversation" not in st.session_state:
        st.session_state.active_conversation = None
    if "uploaded_pdf_text" not in st.session_state:
        st.session_state.uploaded_pdf_text = ""

    with st.sidebar:
        st.header("Conversations")
        extract_text_from_pdf()

        if st.button("New Chat"):
            conversation_id = f"chat_{len(st.session_state.conversations) + 1}"
            st.session_state.conversations[conversation_id] = {
                "title": f"Chat {len(st.session_state.conversations) + 1}", "messages": [],
                "created_at": datetime.now()}
            st.session_state.active_conversation = conversation_id

        for conv_id, conv in st.session_state.conversations.items():
            if st.button(conv["title"]):
                st.session_state.active_conversation = conv_id

    if st.session_state.active_conversation:
        conversation_id = st.session_state.active_conversation
        conversation = st.session_state.conversations[conversation_id]

        st.subheader(conversation["title"])

        for msg in conversation["messages"]:
            st.markdown(f"**You:** {msg['query']}")
            st.markdown(f"**Bot:** {msg['response']}")

        user_query = st.text_input("Ask a question:")
        if st.button("Send") and user_query:
            handle_query(user_query)
    else:
        st.info("Start a new conversation by clicking 'New Chat' or selecting an existing one!")


chat_ui()
