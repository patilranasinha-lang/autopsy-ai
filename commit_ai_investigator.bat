git checkout -b feature/ai-investigator-rag
git add ai_engine/rag/document_chunker.py ai_engine/rag/local_embedder.py
git commit -m "feat: implement behavioral data chunking and embedding"
git add ai_engine/rag/vector_store.py ai_engine/rag/context_retriever.py
git commit -m "feat: add local vector storage and retrieval pipeline"
git add ai_engine/investigator/prompt_manager.py ai_engine/investigator/llm_orchestrator.py
git commit -m "feat: build llm orchestration and system prompts"
git add ai_engine/investigator/conversation_memory.py api/routers/chat_router.py
git commit -m "feat: add chat history and fast-api chat router"
git add models/vector_embedding.py models/chat_history.py
git commit -m "feat: create vector and chat history models"
git add frontend/src/components/ChatWindow.jsx frontend/src/components/EvidenceCard.jsx
git commit -m "feat: build React AI chat interface"
git add tests/rag/ tests/investigator/
git commit -m "test: add ai investigator test suite"
git add ARCHITECTURE.md ROADMAP.md
git commit -m "docs: document RAG and AI investigator architecture"
git add .
git commit -m "feat: complete sprint days 31-40 ai investigator pipeline"
