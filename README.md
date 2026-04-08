# LegalBroom: Harvey-style Legal AI Assistant 🏛️🧹

LegalBroom is a high-precision Legal AI Assistant designed for professional researchers and lawyers. It leverages a powerful RAG (Retrieval-Augmented Generation) pipeline integrated with the **Free Law Project (CourtListener)** to provide real-time, cited legal analysis.

## 🚀 Key Features

- **Live Case Law Research**: Integrated with the CourtListener V4 API to search millions of legal precedents on-demand.
- **Autonomous Search Refinement**: The AI intelligently evaluates initial search results and automatically triggers refined, iterative searches if more context is needed.
- **Deep Case Analysis**: A dedicated `/analysis` interface where users can input complex legal scenarios for multi-step synthesis and relevance grading.
- **Verifiable Citations**: Every claim made by the assistant is backed by clickable `[Source N]` markers that link directly to the original legal records.
- **Real-time Status Streaming**: Granular feedback (e.g., "Searching...", "Grading relevance...", "Synthesizing...") keeps users informed during complex research tasks.
- **Multi-Provider LLM Support**: Built-in `LLMFactory` to seamlessly switch between OpenAI (**GPT-4o-mini**) and local models (**Llama 3 via Ollama**).

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python, LangChain.
- **Frontend**: Next.js, Tailwind CSS, TypeScript.
- **Search API**: CourtListener (Free Law Project).
- **Inference**: OpenAI API or Local Ollama.
- **Testing**: Playwright, Pytest.

## 🚦 Getting Started

### Prerequisites
- Docker & Docker Compose
- API Keys: OpenAI and CourtListener (Free Law Project)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/acethepace/legalbroom.git
   cd legalbroom
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

3. **Start the application**:
   ```bash
   docker compose up -d --build
   ```

4. **Access the UI**:
   Navigate to `http://localhost:3000` in your browser.

## 🧪 Testing

LegalBroom includes a robust automated test suite covering Constitutional, Employment, Corporate, and Administrative law scenarios.

To run the tests:
```bash
pytest tests/legal_queries/
```

## 🤝 Multi-Agent Protocol

This project was built using a specialized multi-agent orchestration workflow:
- **Architect**: Designed the RAG pipeline and citation schema.
- **Coder**: Implemented the FastAPI endpoints and Next.js frontend.
- **Tester**: Verified UI and search relevance using Playwright.
- **Debugger**: Root-cause diagnosis and performance optimization.

---
*Disclaimer: This tool is for research assistance only and does not constitute legal advice.*
