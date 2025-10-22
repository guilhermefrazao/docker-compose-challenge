# 💬 Document QA Frontend (Streamlit)

Este é o **frontend** do sistema de perguntas e respostas sobre documentos.  
Ele fornece uma interface simples de chat que se comunica com o **backend FastAPI**.

---

## 🚀 Funcionalidades

- Upload de documentos (PDF/TXT)
- Envio de perguntas
- Respostas geradas em tempo real (streaming)
- Interface amigável em **Streamlit**

---

## ⚙️ Instalação

### 1️⃣ Criar ambiente virtual (opcional)
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
````

### 2️⃣ Instalar dependências

```bash
pip install streamlit requests
```

---

## ▶️ Execução

### 3️⃣ Iniciar o aplicativo Streamlit

```bash
streamlit run app.py
```

O app abrirá automaticamente em:

> **[http://localhost:8501](http://localhost:8501)**

---

## 🔗 Configuração de conexão

O app se comunica com o backend definido em:

```python
backend_url = "http://localhost:9000"
```

Se o backend estiver rodando em outro host ou porta, basta alterar essa variável no código `app.py`.

---

## 🧠 Fluxo de uso

1. Envie um arquivo PDF ou TXT.
2. Aguarde a confirmação de upload.
3. Digite uma pergunta sobre o conteúdo.
4. Veja a resposta sendo construída em tempo real! ⚡

---

## 📁 Estrutura

```
frontend/
├── app.py          # Código principal do frontend
├── README.md       # Este arquivo
```

---

## 🧩 Exemplo de uso

1. Suba o backend FastAPI:

   ```bash
   uvicorn server:app --reload --port 9000
   ```

2. Execute o frontend:

   ```bash
   streamlit run app.py
   ```

3. No navegador:

   * Faça upload de um documento.
   * Escreva sua pergunta.
   * Veja a resposta aparecer gradualmente! 🧠💬

```
