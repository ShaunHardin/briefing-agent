# Briefing Agent Project

## Overview
This is a learning project to build a Newsletter Digest Agent that reads newsletters from Gmail, synthesizes insights, and provides personalized learning recommendations.

**Repository**: https://github.com/ShaunHardin/briefing-agent

**Goal**: Go from "I understand what RAG is" → "I shipped an AI product that customers love"

## Current State
**Phase**: Foundation - Gmail Connection Test ✅

### Completed Features
- ✅ Python 3.11 environment setup
- ✅ Gmail API integration with OAuth support
- ✅ Test suite following TDD practices (6 passing tests)
- ✅ Email fetcher with query filtering support
- ✅ Demo script for testing Gmail connection
- ✅ Automated test workflow

### Test Coverage
All tests passing (6/6):
- Gmail fetcher initialization
- Email retrieval (with and without results)
- Email data structure validation
- Error handling
- Query filtering

## Project Architecture

### Directory Structure
```
/agent      → Core agent logic (gmail_fetcher.py)
/evals      → Test suite (test_gmail.py)
/data       → OAuth credentials and tokens (gitignored)
```

### Tech Stack
- **Language**: Python 3.11
- **Gmail API**: OAuth 2.0 authentication
- **Testing**: pytest with mocking
- **Future**: FAISS, OpenAI, Streamlit

### Key Components
1. **GmailFetcher** (`agent/gmail_fetcher.py`): 
   - Handles OAuth authentication
   - Fetches emails with query support
   - Parses email headers and body
   
2. **Test Suite** (`evals/test_gmail.py`):
   - TDD approach - tests written first
   - Mocked Gmail API for reliable testing
   - Covers initialization, fetching, and error handling

## Setup Required
Users need to complete OAuth setup to use the demo script:
1. Create Google Cloud project
2. Enable Gmail API
3. Download OAuth credentials → `data/credentials.json`
4. See SETUP.md for detailed instructions

## Next Steps
### Immediate
- User completes OAuth setup
- Test live Gmail connection with demo script
- Verify ability to filter newsletters

### Future Features (Planned)
- FAISS vector storage for newsletters
- OpenAI integration for synthesis
- Personalized learning memory
- Attention scoring system
- Weekly digest generation
- Eval framework for relevance metrics
- Streamlit UI for feedback

## Recent Changes
- **October 19, 2025**: 
  - Set up Python environment
  - Built Gmail fetcher with TDD approach
  - Created test suite (6 passing tests)
  - Added OAuth setup documentation
  - Configured test workflow
- **October 15, 2025**: Repository imported to Replit
- **October 14, 2025**: Initial commit with LICENSE file

## User Preferences
- **Development Approach**: TDD (test-driven development)
- **LLM Provider**: OpenAI (via Replit AI Integrations)
- **Email Source**: Gmail with OAuth
- **Testing**: pytest with comprehensive test harness
