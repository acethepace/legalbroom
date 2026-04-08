# LegalBroom: Harvey-style Legal AI Assistant 🏛️🧹

LegalBroom is a high-precision Legal AI Assistant designed for professional researchers and lawyers. It leverages a powerful RAG (Retrieval-Augmented Generation) pipeline integrated with the **Free Law Project (CourtListener)** to provide real-time, cited legal analysis.

## 🖼️ Examples & Gallery

LegalBroom is designed to handle both quick inquiries and deep, multi-step case analysis. Below are visual walkthroughs of its primary features.

### 1. Deep Case Analysis (Multi-Step RAG)
In this workflow, the AI extracts search queries from a complex scenario, retrieves cases, grades their relevance, and provides a final synthesis.

- **Scenario**: *Warrantless search of a vehicle glove compartment during a minor traffic stop.*
- **Outcome**: The AI identifies the scope of *Terry* stops and retrieves relevant Fourth Amendment precedents.

| Step | View | Description |
|------|------|-------------|
| **Input** | ![Case Details Input](https://screenshot.gemini.autonome.ai/analysis_input_constitutional.png) | Lawyer enters detailed facts and legal questions. |
| **Grading** | ![Relevance Grading](https://screenshot.gemini.autonome.ai/analysis_processing_constitutional.png) | AI evaluates multiple CourtListener results for relevance. |
| **Analysis** | ![Final Analysis](https://screenshot.gemini.autonome.ai/analysis_result_constitutional.png) | Final synthesized report with filtered citations. |

### 2. General Legal Search
Quickly find information on specific legal doctrines or landmark cases directly from the dashboard.

- **Query**: *"What are the Miranda rights?"*
- **Outcome**: A concise summary of the Fifth Amendment protections with direct links to foundational case law.

| Feature | View | Description |
|---------|------|-------------|
| **Search Result** | ![Miranda Search Result](https://screenshot.gemini.autonome.ai/search_result_miranda.png) | Synthesis of search results with integrated citations. |
| **Citation Details** | ![Citation View](https://screenshot.gemini.autonome.ai/citation_details_highlighted_miranda.png) | Sidebar showing metadata and case snippets. |

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
