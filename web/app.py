import streamlit as st
import requests
import os

st.title("Document QA - Chat com RAG (vLLM + ChromaDB)")

backend_url = os.getenv("API_URL", "http://localhost:9000")  

uploaded_file = st.file_uploader("📄 Envie um documento (PDF ou TXT):", type=["pdf", "txt"])
if uploaded_file:
    with st.spinner("Enviando documento..."):
        files = {"file": uploaded_file}
        resp = requests.post(f"{backend_url}/upload", files=files)
        if resp.status_code == 200:
            st.success("Documento enviado e indexado com sucesso!")
        else:
            st.error("Erro ao enviar o documento.")

question = st.text_input("❓ Faça uma pergunta sobre o documento:")
if st.button("Enviar") and question:
    with st.spinner("Gerando resposta..."):
        response = requests.post(f"{backend_url}/ask", data={"question": question}, stream=True)
        if response.status_code == 200:
            answer = ""
            placeholder = st.empty()
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    answer += chunk.decode("utf-8")
                    placeholder.markdown(answer)
        else:
            st.error("Erro ao se comunicar com o servidor.")
