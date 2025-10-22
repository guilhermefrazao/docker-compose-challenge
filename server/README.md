# 🧠 Document QA API (FastAPI + ChromaDB + vLLM)

Este serviço é o **backend** do sistema de perguntas e respostas com base em documentos.  
Ele gerencia o armazenamento de textos no **ChromaDB**, a busca de trechos relevantes e a comunicação com o **modelo de linguagem (vLLM)**.

---

## 🚀 Funcionalidades

- Recebe documentos PDF ou TXT via upload.
- Extrai e armazena o conteúdo no **ChromaDB**.
- Realiza busca semântica dos trechos mais relevantes para uma pergunta.
- Faz streaming da resposta gerada pelo **modelo LLM (vLLM)**.

---

## 🧩 Tecnologias utilizadas

- **FastAPI** — Framework web rápido e assíncrono.
- **ChromaDB** — Banco vetorial local.
- **LangChain** — Para dividir o texto em chunks.
- **PyPDF2** — Extração de texto de PDFs.
- **vLLM / Unsloth** — Modelo de linguagem para responder perguntas.

---

## ⚙️ Instalação

### 1️⃣ Criar ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
````

### 2️⃣ Instalar dependências

```bash
pip install fastapi uvicorn requests PyPDF2 langchain chromadb
```

---

## ▶️ Execução

### 3️⃣ Iniciar o servidor

```bash
uvicorn server:app --host 0.0.0.0 --port 9000 --reload
```

O servidor iniciará em:

> **[http://localhost:9000](http://localhost:9000)**

---

## 📡 Endpoints

### **POST /upload**

Envia um documento (PDF ou TXT) para ser armazenado no ChromaDB.

**Exemplo via `curl`:**

```bash
curl -X POST -F "file=@meu_arquivo.pdf" http://localhost:9000/upload
```

---

### **POST /ask**

Faz uma pergunta com base no documento armazenado.

**Exemplo via `curl`:**

```bash
curl -X POST -F "question=Qual é o objetivo do texto?" http://localhost:9000/ask
```

A resposta será transmitida em **streaming** (texto contínuo).

---

## 🧠 Arquitetura Simplificada

```
+-------------+        +------------+        +-------------+
|  Streamlit  |  --->  |  FastAPI   |  --->  |   vLLM API  |
|   Frontend  |         |  Backend   |        | (localhost) |
+-------------+        +------------+        +-------------+
        |                        |
        |<------ Contexto -------|
        |<----- Resposta --------|
```

---

## 📁 Estrutura

```
server/
├── server.py       # Código principal do backend
├── README.md       # Este arquivo
```

---

## 🧩 Requisitos adicionais

* Um servidor **vLLM** rodando em `http://localhost:8000/v1/chat/completions`.
* Python 3.9+.

---

## ✅ Exemplo de uso completo

1. Suba o servidor:

   ```bash
   uvicorn server:app --reload --port 9000
   ```
2. Faça upload de um documento:

   ```bash
   curl -X POST -F "file=@documento.pdf" http://localhost:9000/upload
   ```
3. Faça uma pergunta:

   ```bash
   curl -X POST -F "question=Qual é o resumo do documento?" http://localhost:9000/ask
   ```

