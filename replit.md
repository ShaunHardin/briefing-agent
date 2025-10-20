# Briefing Agent Project

## Overview
This is a learning project to build a Newsletter Digest Agent that reads newsletters from Gmail, synthesizes insights, and provides personalized learning recommendations.

**Repository**: https://github.com/ShaunHardin/briefing-agent

**Goal**: Go from "I understand what RAG is" → "I shipped an AI product that customers love"

## Current State
**Phase**: Foundation - Gmail Connection ✅ LIVE & WORKING

### Completed Features
- ✅ Python 3.11 environment setup
- ✅ Gmail API integration with OAuth 2.0 authentication
- ✅ Successfully connected to user's Gmail account
- ✅ Test suite following TDD practices (10 passing tests)
- ✅ Email fetcher with query filtering support
- ✅ Recursive multipart email parsing (handles real newsletters)
- ✅ Demo script verified with live Gmail data
- ✅ Automated test workflow

### Test Coverage
All tests passing (10/10):
- Gmail fetcher initialization
- Email retrieval (with and without results)
- Email data structure validation
- Error handling
- Query filtering with parameters
- Multipart/alternative email parsing
- HTML-only email handling
- Deeply nested multipart structures
- HTTP error handling

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

## OAuth Setup Status
✅ **Complete** - Gmail API authenticated and working
- OAuth credentials configured
- Access token saved in `data/token.json`
- Successfully fetching live emails from Gmail
- Token refreshes automatically (7-day expiry in Testing mode)

## Next Steps
### Immediate
- Filter newsletters specifically (e.g., from Substack, Maven, etc.)
- Start building newsletter storage and synthesis features

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
