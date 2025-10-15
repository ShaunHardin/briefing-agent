# Newsletter Digest Agent 2.0

## Overview
A personalized AI research companion that reads newsletters from Gmail, synthesizes insights, and coaches learning by surfacing trends, generating personalized challenges, and tracking engagement.

**Purpose**: Transform newsletter overload into actionable learning insights  
**Current State**: MVP functional with Gmail integration, AI synthesis, and Streamlit UI  
**Tech Stack**: Python, Streamlit, OpenAI (via Replit AI Integrations), Gmail API, FAISS

## Recent Changes
- **October 15, 2025**: 
  - Set up Python environment with all dependencies
  - Configured Gmail and OpenAI integrations
  - Built newsletter fetcher with Gmail API
  - Implemented AI synthesis agent for insight extraction
  - Created Streamlit UI for digest viewing
  - Added FAISS vector store for newsletter memory (placeholder embeddings)
  - Built basic evaluation framework
  - Configured workflow and deployed to port 5000

## Project Architecture

### Directory Structure
```
/agent          - Core agent logic
  ├── gmail_client.py    - Gmail API integration
  ├── synthesizer.py     - AI synthesis with OpenAI
  └── memory.py          - FAISS vector store for newsletter memory

/evals          - Evaluation framework
  └── eval_framework.py  - Metrics for relevance, completeness, actionability

/data           - Storage for FAISS index and metadata
  ├── newsletter_index.faiss
  └── newsletter_metadata.json

app.py          - Streamlit UI application
```

### Core Components

1. **Gmail Integration** (`agent/gmail_client.py`)
   - Fetches newsletters using Gmail API with OAuth
   - Supports custom search queries and auto-detection
   - Extracts and cleans email content

2. **AI Synthesis** (`agent/synthesizer.py`)
   - Uses OpenAI (gpt-4o-mini) via Replit AI Integrations
   - Generates summaries, insights, trends, and action items
   - Creates personalized learning prompts

3. **Vector Memory** (`agent/memory.py`)
   - FAISS-based vector store for newsletter embeddings
   - Enables semantic search across past newsletters
   - Note: Currently uses placeholder embeddings (OpenAI embeddings API not supported by AI Integrations)

4. **Evaluation Framework** (`evals/eval_framework.py`)
   - Measures relevance, completeness, and actionability
   - Saves evaluation results for continuous improvement

5. **Streamlit UI** (`app.py`)
   - Web interface for viewing digests
   - Feedback collection system
   - Newsletter browsing and search

### Integrations
- **Gmail**: OAuth connection for email access (read-only permissions)
- **OpenAI**: Replit AI Integrations (no API key needed, billed to credits)

### Key Features Implemented
- ✅ Newsletter fetching from Gmail
- ✅ AI-powered insight synthesis
- ✅ Trend identification
- ✅ Personalized learning prompts
- ✅ Basic vector memory with FAISS
- ✅ Evaluation metrics
- ✅ User feedback collection

### Planned Enhancements
- [ ] Proper embeddings (when supported by AI Integrations)
- [ ] Attention scoring based on user engagement
- [ ] Insight graph visualization
- [ ] Advanced evals with Phoenix/DeepEval/TruLens
- [ ] Privacy controls with PII detection
- [ ] LangGraph orchestration (if needed for complex workflows)

## User Preferences
- **Learning Style**: Self-guided with AI coaching
- **Focus**: Building AI products end-to-end (design, evals, safety, strategy)
- **Data Source**: Gmail newsletters
- **Privacy**: Important consideration for future iterations

## How to Use

1. **Fetch Newsletters**: Click "Fetch & Analyze" in the sidebar
2. **Review Digest**: See AI-generated summary, insights, and trends
3. **Get Learning Prompts**: Click on insights to generate personalized challenges
4. **Provide Feedback**: Share what's useful to improve future digests

## Technical Notes

- Server runs on port 5000 (Streamlit with `--server.address=0.0.0.0`)
- Gmail connection uses Replit Connectors with automatic token refresh
- OpenAI uses Replit AI Integrations (gpt-4o-mini model)
- FAISS index stored in `/data` directory
- Evaluation results saved to `/evals/results.json`
