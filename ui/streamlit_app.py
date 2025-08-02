# import streamlit as st
# import requests
# import tempfile
# import os

# API_URL = "http://localhost:8000/api"

# st.title("📄 RAG Chatbot")

# uploaded_files = st.sidebar.file_uploader(
#     "Upload CVs or docs", accept_multiple_files=True, type=["pdf", "docx", "txt"]
# )

# if uploaded_files:
#     temp_paths = []
#     for f in uploaded_files:
#         tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(f.name)[1])
#         tmp.write(f.getbuffer())
#         tmp.close()
#         temp_paths.append(tmp.name)
#     if st.sidebar.button("Ingest Documents"):
#         with st.spinner("Ingesting documents…"):
#             resp = requests.post(f"{API_URL}/ingest", json={"files": temp_paths})
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
#         st.markdown("**Source Chunks:**")
#         for src in data["source_docs"]:
#             st.write(src)
#     else:
#         st.error(f"API Error: {resp.text}")



import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.title("📄 RAG Chatbot")

uploaded_files = st.sidebar.file_uploader(
    "Upload CVs or docs", accept_multiple_files=True, type=["pdf", "docx", "txt"]
)

if uploaded_files:
    if st.sidebar.button("Ingest Documents"):
        with st.spinner("Ingesting documents…"):
            # Prepare files for multipart/form-data upload
            files = [
                ("files", (f.name, f, f.type or "application/octet-stream"))
                for f in uploaded_files
            ]

            resp = requests.post(f"{API_URL}/ingest", files=files)

        if resp.ok:
            st.sidebar.success("Ingestion successful!")
        else:
            st.sidebar.error(f"Error: {resp.text}")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question", key="query_input")
if st.button("Send") and query:
    with st.spinner("Getting answer…"):
        resp = requests.post(f"{API_URL}/chat", json={"query": query})
    if resp.ok:
        data = resp.json()
        st.session_state.history.append((query, data["response"]))
        for msg, ans in st.session_state.history:
            st.markdown(f"**You:** {msg}")
            st.markdown(f"**Bot:** {ans}")
        st.markdown("---")
        # st.markdown("**Source Chunks:**")
        # for src in data["source_docs"]:
        #     st.write(src)
    else:
        st.error(f"API Error: {resp.text}")
