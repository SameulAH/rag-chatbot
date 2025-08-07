# import streamlit as st
# import requests

# API_URL = "http://localhost:8000/api"

# st.title("📄 RAG Chatbot")

# uploaded_files = st.sidebar.file_uploader(
#     "Upload CVs or docs", accept_multiple_files=True, type=["pdf", "docx", "txt"]
# )

# if uploaded_files:
#     if st.sidebar.button("Ingest Documents"):
#         with st.spinner("Ingesting documents…"):
#             # Prepare files for multipart/form-data upload
#             files = [
#                 ("files", (f.name, f, f.type or "application/octet-stream"))
#                 for f in uploaded_files
#             ]

#             resp = requests.post(f"{API_URL}/ingest", files=files)

#         if resp.ok:
#             st.sidebar.success("Ingestion successful!")
#         else:
#             st.sidebar.error(f"Error: {resp.text}")

# if "history" not in st.session_state:
#     st.session_state.history = []

# query = st.text_input("Ask a question", key="query_input")
# if st.button("Send") and query:
#     with st.spinner("Getting answer…"):
#         resp = requests.post(f"{API_URL}/chat", json={"query": query})
#     if resp.ok:
#         data = resp.json()
#         st.session_state.history.append((query, data["response"]))
#         for msg, ans in st.session_state.history:
#             st.markdown(f"**You:** {msg}")
#             st.markdown(f"**Bot:** {ans}")
#         st.markdown("---")
#         # st.markdown("**Source Chunks:**")
#         # for src in data["source_docs"]:
#         #     st.write(src)
#     else:
#         st.error(f"API Error: {resp.text}")


import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="RAG Chat", page_icon="📄")
st.title("📄 You assistant can help ...")

uploaded_files = st.sidebar.file_uploader(
    "Upload your docs", accept_multiple_files=True, type=["pdf", "docx", "txt"]
)

# Ingest files with multipart/form-data
if uploaded_files:
    if st.sidebar.button("Ingest Documents"):
        with st.spinner("Ingesting documents…"):
            files = [
                ("files", (f.name, f, f.type or "application/octet-stream"))
                for f in uploaded_files
            ]
            resp = requests.post(f"{API_URL}/ingest", files=files)

        if resp.ok:
            st.sidebar.success("Ingestion successful!")
        else:
            st.sidebar.error(f"Error: {resp.text}")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List of {"role": "user"/"bot", "content": str}

# Chat UI
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Bot:** {msg['content']}")

# Input box
user_input = st.text_input("Your message", key="chat_input")

if st.button("Send") and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare full conversation for API
    chat_payload = {
        "messages": [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_history
        ]
    }

    with st.spinner("Thinking…"):
        response = requests.post(f"{API_URL}/chat", json=chat_payload)

    if response.ok:
        reply = response.json()["response"]
        st.session_state.chat_history.append({"role": "bot", "content": reply})
        st.rerun()
    else:
        st.error(f"API Error: {response.text}")

