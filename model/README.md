# 🧠 Servidor vLLM com Docker (CPU)

Este comando executa um **servidor vLLM** em um contêiner Docker para servir modelos de linguagem de forma rápida e eficiente, sem precisar instalar dependências locais de IA.  
O exemplo abaixo usa o modelo **Qwen2-1.5B-Instruct**, que é leve e otimizado para rodar em CPU.

---

## 🚀 O que é o vLLM?

O **vLLM** é um **servidor de inferência otimizado para LLMs (Large Language Models)**.  
Ele fornece uma **API compatível com o padrão OpenAI** (`/v1/chat/completions`), permitindo usar bibliotecas como `requests`, `LangChain`, ou `OpenAI SDK` para se comunicar com o modelo — assim como se fosse a API oficial da OpenAI, mas rodando **localmente**.

---

## 🐳 Comando para executar


```bash
cd model

bash vllm-cpu.sh
````


```bash
docker run -it \
  --rm \
  --network=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm-cpu-env \
  --model Qwen/Qwen2-1.5B-Instruct \
  --trust-remote-code \
  --device cpu \
  --dtype bfloat16 \
  --tokenizer-mode auto
````

---

## ⚙️ Explicação dos parâmetros

| Flag / Opção                                       | Descrição                                                                                                      |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `docker run -it`                                   | Executa o contêiner em modo interativo.                                                                        |
| `--rm`                                             | Remove o contêiner automaticamente ao final da execução.                                                       |
| `--network=host`                                   | Usa a rede do host, permitindo acesso direto via `localhost`. Ideal para servir a API localmente.              |
| `-v ~/.cache/huggingface:/root/.cache/huggingface` | Monta o cache local do Hugging Face para evitar baixar o modelo novamente a cada execução.                     |
| `vllm-cpu-env`                                     | Nome da imagem Docker (deve conter o ambiente vLLM configurado).                                               |
| `--model Qwen/Qwen2-1.5B-Instruct`                 | Define o modelo a ser carregado.                                                                               |
| `--trust-remote-code`                              | Permite carregar código customizado do repositório do modelo (necessário para alguns modelos da Hugging Face). |
| `--device cpu`                                     | Define que o modelo será executado na CPU.                                                                     |
| `--dtype bfloat16`                                 | Tipo de dado usado na inferência (bfloat16 reduz o uso de memória).                                            |
| `--tokenizer-mode auto`                            | Deixa o vLLM escolher o melhor modo de tokenização automaticamente.                                            |

---

## 📡 Endpoint gerado

Após iniciar, o vLLM expõe um servidor HTTP compatível com OpenAI API:

```
http://localhost:8000/v1/chat/completions
```

Você pode testar com um `curl` ou com Python.

### Exemplo com `curl`:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2-1.5B-Instruct",
    "messages": [
      {"role": "system", "content": "Você é um assistente útil."},
      {"role": "user", "content": "Explique o que é o vLLM."}
    ]
  }'
```

### Exemplo com Python:

```python
import requests

url = "http://localhost:8000/v1/chat/completions"
payload = {
    "model": "Qwen/Qwen2-1.5B-Instruct",
    "messages": [
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Explique o que é o vLLM."}
    ]
}
response = requests.post(url, json=payload)
print(response.json())
```

---

## 🧩 Requisitos

* Docker instalado e funcionando.
* A imagem `vllm-cpu-env` deve estar disponível localmente ou no registro Docker.
* Conexão com a internet (apenas no primeiro download do modelo).

---

## 💡 Dica

Se quiser usar uma GPU (quando disponível), basta trocar:

```bash
--device cpu
```

por

```bash
--device cuda
```

E garantir que a imagem do Docker tenha suporte a CUDA.

---

## ✅ Exemplo de integração com outro sistema

Você pode conectar esse servidor ao seu backend (como o FastAPI usado no projeto RAG):

```python
url = "http://localhost:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}
payload = {
    "model": "Qwen/Qwen2-1.5B-Instruct",
    "messages": [
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Resuma o conteúdo do documento."}
    ]
}
response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

---

## 🧠 Resumo

| Tarefa              | Descrição                                   |
| ------------------- | ------------------------------------------- |
| 🔧 Subir o servidor | Executar o comando Docker acima             |
| 🌐 Endpoint local   | `http://localhost:8000/v1/chat/completions` |
| 💬 Modelo usado     | `Qwen/Qwen2-1.5B-Instruct`                  |
| ⚙️ Ambiente         | CPU (modo leve)                             |
| 📦 Persistência     | Cache de modelos em `~/.cache/huggingface`  |

---

## 🏁 Conclusão

Esse comando permite executar um modelo de linguagem localmente com **vLLM** e **Docker**, servindo uma API OpenAI-compatível em poucos segundos — sem precisar configurar ambientes complexos de machine learning.

```

---

Deseja que eu gere também o **Dockerfile** correspondente à imagem `vllm-cpu-env` (para você construir localmente)?  
Assim você poderia montar seu próprio ambiente vLLM customizado.
