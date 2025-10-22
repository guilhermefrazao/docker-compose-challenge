from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from PyPDF2 import PdfReader
from langchain_text_splitters import  CharacterTextSplitter
import chromadb
import requests
import json
import io

app = FastAPI(title="Document QA API")

prompt_template = """
Você é um assistente que precisa responder às dúvidas de um usuário com base em um documento fornecido como contexto.

Esse é o documento:
{context}

Essa é a pergunta do usuário:
{question}

Responda a pergunta do usuário com base no documento fornecido.
"""

# --- Funções utilitárias --- #
def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    pdf_reader = PdfReader(io.BytesIO(pdf_file.file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def store_document_in_chroma(client, document_text, collection_name="documents"):
    text_splitter = CharacterTextSplitter(chunk_size=128, chunk_overlap=0)
    texts = text_splitter.split_text(document_text)
    collection = client.get_or_create_collection(name=collection_name)
    collection.add(
        documents=texts,
        metadatas=[{"source": "uploaded_pdf"}] * len(texts),
        ids=[f"doc_{i}" for i in range(len(texts))]
    )

def retrieve_relevant_documents(client, question, collection_name="documents", n_results=1):
    collection = client.get_collection(name=collection_name)
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    return results["documents"]

def stream_llm_response(prompt: str):
    url = "http://localhost:8000/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "unsloth/Qwen3-8B-bnb-4bit",
        "messages": [
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": prompt},
        ],
        "stream": True,
        "max_tokens": 2048
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True)
    if response.status_code != 200:
        yield "Erro ao obter resposta do modelo."
        return

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            if decoded_line.startswith("data:"):
                data = decoded_line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    content = chunk["choices"][0]["delta"].get("content", "")
                    if content:
                        yield content
                except json.JSONDecodeError:
                    continue

@app.post("/upload")
async def upload_document(file: UploadFile):
    client = chromadb.Client()
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    else:
        text = (await file.read()).decode("utf-8")
    store_document_in_chroma(client, text)
    return JSONResponse({"message": "Documento armazenado com sucesso!"})

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    client = chromadb.Client()
    context = retrieve_relevant_documents(client, question)
    prompt = prompt_template.format(context=context, question=question)
    return StreamingResponse(stream_llm_response(prompt), media_type="text/plain")
