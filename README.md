# Newsletter Digest Agent 2.0

An AI-powered assistant that reads Gmail newsletters, synthesizes insights, and provides personalized learning recommendations.

> **Learning Project**: Master the full AI product lifecycle - design, evals, deployment, and strategy.

## Overview

This agent helps you:
- 📧 Fetch newsletters from Gmail automatically
- 🧠 Synthesize key insights using AI
- 📚 Build personalized learning memory
- 📊 Score content by attention-worthiness
- 📮 Deliver weekly digests with actionable recommendations

## Current Status

**Phase**: Foundation - Gmail Connection ✅ LIVE & WORKING

See [PLAN.md](PLAN.md) for detailed roadmap and progress.

## Features

### ✅ Completed
- Gmail API integration with OAuth 2.0 authentication
- Email fetching with query filtering (by sender, label, keywords)
- Recursive multipart email parser (handles real-world newsletters)
- Comprehensive test suite (10 passing tests)
- Successfully tested with live Gmail data

### 🚧 In Progress
- Newsletter-specific filtering
- AI-powered synthesis pipeline

### 📋 Planned
- FAISS vector storage for newsletter content
- OpenAI integration for content synthesis
- Personalized learning memory system
- Attention scoring algorithm
- Weekly digest generation
- Evaluation framework for relevance metrics
- Streamlit UI for user feedback

## Quick Start

### Prerequisites
- Python 3.11
- Gmail account
- Google Cloud project with Gmail API enabled

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ShaunHardin/briefing-agent.git
cd briefing-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Gmail OAuth**

Follow the detailed instructions in [SETUP.md](SETUP.md) to:
- Create a Google Cloud project
- Enable Gmail API
- Download OAuth credentials
- Authenticate your Gmail account

4. **Test the connection**
```bash
python demo_gmail_connection.py
```

### Running Tests

```bash
pytest evals/test_gmail.py -v
```

## Project Structure

```
briefing-agent/
├── agent/              # Core agent logic
│   └── gmail_fetcher.py    # Gmail API integration
├── evals/              # Test suite
│   └── test_gmail.py       # Unit tests with mocking
├── data/               # OAuth credentials & tokens (gitignored)
│   ├── credentials.json    # OAuth client secret
│   └── token.json          # Access/refresh tokens
├── PLAN.md             # Project roadmap and progress
├── SETUP.md            # OAuth setup instructions
└── demo_gmail_connection.py  # Demo script
```

## Tech Stack

- **Language**: Python 3.11
- **Email Integration**: Gmail API with OAuth 2.0
- **Testing**: pytest with mocking
- **Planned**: 
  - FAISS (vector storage)
  - OpenAI (content synthesis via Replit AI Integrations)
  - LangGraph/AgentKit (agent orchestration)
  - Streamlit (UI)

## Development Approach

This project follows **Test-Driven Development (TDD)**:
1. Write tests first
2. Implement features to pass tests
3. Refactor with confidence

All code changes are backed by comprehensive test coverage.

## Documentation

- [PLAN.md](PLAN.md) - Project roadmap and detailed progress
- [SETUP.md](SETUP.md) - Gmail OAuth setup guide
- [replit.md](replit.md) - Replit-specific configuration and preferences

## Contributing

This is a personal learning project, but feedback and suggestions are welcome! Feel free to open an issue or reach out.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Learning Goals

This project is designed to teach:
- Building production-grade AI applications
- Test-driven development for ML/AI systems
- Evaluation frameworks for AI agents
- RAG (Retrieval Augmented Generation) architecture
- Agent orchestration with LangGraph
- Full product lifecycle: design → build → eval → deploy

---

**Status**: 🟢 Active Development | **Phase**: Foundation (Gmail Integration Complete)
