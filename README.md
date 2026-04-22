# 🚀 DocAgent

**DocAgent** is an AI-powered web crawler and document interaction tool that allows you to crawl any website, extract its content, and interact with it using Large Language Models (LLMs).

> Turn any webpage into a queryable knowledge base.

---

## ✨ Features

- 🌐 Crawl any website via URL
- 📄 Extract and clean webpage content
- ✂️ Intelligent text chunking
- 🔍 Semantic retrieval of relevant content
- 🤖 Ask questions using LLMs (OpenAI / Ollama compatible)
- ⚡ Interactive UI built with Streamlit
- 🔌 Modular LLM provider support

---

## 🏗️ Project Structure

docAgent/
├─ app/ # Streamlit UI & app state
├─ core/ # Core logic (crawler, chunking, retrieval)
├─ llm/ # LLM provider integrations
├─ utils/ # Helper utilities
├─ tests/ # Unit tests
├─ .env.example # Environment variables template
├─ requirements.txt # Dependencies
└─ README.md



---

## ⚙️ How It Works

1. Enter a website URL
2. Crawl and extract content
3. Split content into chunks
4. Store embeddings
5. Ask questions
6. Retrieve relevant chunks
7. Generate answers using LLM

---

## 🧠 Supported LLM Providers

- OpenAI-compatible APIs
- Ollama (local models)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/docAgent.git
cd docAgent


