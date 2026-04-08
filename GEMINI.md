# Project: Harvey-style Legal AI Assistant

## Tech Stack
- Backend: Python/FastAPI + LangChain
- Vector Store: Qdrant (Local Docker)
- Frontend: Next.js + Tailwind

## Multi-Agent Protocol (Autonomous)
- **Architect:** Design the RAG pipeline and citation schema.
- **Coder:** Implement the FastAPI endpoints and Next.js frontend.
- **Tester (Computer Use):** Once the Coder finishes a feature, the Tester must launch the local dev server, open Chrome via BrowserMCP, and verify the UI.
- **Security:** Audit all document ingestion scripts for PII masking.

## Tester Agent Instructions (MCP)
The Tester has access to `mcp_browser_*` tools. 
- Goal: Ensure the "Upload PDF" button works and the "Citations" pane appears after a query.
- Constraint: If a test fails, the Tester must hand the logs back to the Coder agent automatically.
