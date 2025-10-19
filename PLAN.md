# Newsletter Digest Agent 2.0 - Project Plan

**Last Updated**: October 19, 2025

## Project Vision

Build an AI-powered newsletter digest agent that transforms email newsletters into personalized learning insights. This is a capstone project to master the full AI product lifecycle: design, evaluation, deployment, and strategy.

## Goals

### Primary Goal
Go from "I understand what RAG is" → "I shipped an AI product that customers love"

### Learning Objectives
- Master RAG (Retrieval Augmented Generation) architecture
- Build production-grade AI applications with proper eval loops
- Practice test-driven development for AI systems
- Understand agent orchestration with LangGraph/AgentKit
- Deploy and iterate based on real user feedback

## Architecture Overview

```
Newsletter → Gmail API → Email Parser → RAG Pipeline → AI Synthesis → Weekly Digest
                                           ↓
                                    Vector Storage (FAISS)
                                           ↓
                                    Learning Memory
                                           ↓
                                    Attention Scoring
```

## Development Phases

### Phase 1: Foundation - Gmail Connection ✅ COMPLETE

**Goal**: Successfully connect to Gmail and fetch newsletter emails

**Completed Tasks**:
- [x] Set up Python 3.11 environment
- [x] Create project structure (/agent, /evals, /data)
- [x] Implement Gmail API integration with OAuth 2.0
- [x] Build recursive multipart email parser
- [x] Write comprehensive test suite (10 passing tests)
- [x] Test with live Gmail data
- [x] Configure automated test workflow
- [x] Document OAuth setup process

**Key Achievements**:
- Successfully authenticated with Gmail API
- Fetched and parsed real-world newsletters
- Handles complex multipart/alternative email formats
- Robust error handling with proper logging
- Test coverage for initialization, fetching, parsing, edge cases

**Files Created**:
- `agent/gmail_fetcher.py` - Core Gmail integration
- `evals/test_gmail.py` - Test suite with mocking
- `demo_gmail_connection.py` - Connection verification script
- `SETUP.md` - OAuth setup guide
- `.gitignore` - Secrets management

**Lessons Learned**:
- TDD approach caught critical bug early: initial parser didn't handle nested multipart structures
- Gmail OAuth "Testing" mode works great for learning projects (7-day token expiry acceptable)
- Architect review process invaluable for catching edge cases

---

### Phase 2: Newsletter Filtering 🚧 IN PROGRESS

**Goal**: Filter and identify newsletter emails specifically

**Tasks**:
- [ ] Identify common newsletter patterns (Substack, Beehiiv, Maven, etc.)
- [ ] Build newsletter detection logic (sender domains, headers)
- [ ] Add label-based filtering (e.g., "Newsletters")
- [ ] Create newsletter metadata extraction (sender, subject, date)
- [ ] Write tests for newsletter filtering
- [ ] Verify with user's actual newsletter subscriptions

**Success Criteria**:
- Accurately identifies 95%+ of newsletters vs regular emails
- No false positives (doesn't flag personal emails as newsletters)
- Handles various newsletter platforms

---

### Phase 3: Content Extraction & Storage 📋 PLANNED

**Goal**: Extract and store newsletter content for retrieval

**Tasks**:
- [ ] Extract article content from newsletter HTML
- [ ] Clean and normalize text (remove ads, footers, etc.)
- [ ] Set up FAISS vector database
- [ ] Generate embeddings for newsletter content
- [ ] Implement chunking strategy for long newsletters
- [ ] Build storage layer with metadata
- [ ] Create retrieval interface for querying stored content
- [ ] Write tests for extraction and storage

**Technical Decisions**:
- **FAISS**: Lightweight, local-first vector storage
- **Chunking Strategy**: TBD (sentence-based? paragraph-based?)
- **Embedding Model**: TBD (OpenAI? Local model?)

---

### Phase 4: AI Synthesis Pipeline 📋 PLANNED

**Goal**: Use AI to synthesize insights from newsletters

**Tasks**:
- [ ] Set up OpenAI integration (via Replit AI Integrations)
- [ ] Design synthesis prompts (extract key insights, themes, learnings)
- [ ] Build content summarization pipeline
- [ ] Implement topic clustering across newsletters
- [ ] Extract actionable recommendations
- [ ] Write tests for synthesis quality
- [ ] Create eval metrics for insight relevance

**Technical Decisions**:
- **LLM**: OpenAI via Replit AI Integrations (no API key needed)
- **Orchestration**: LangGraph if needed for complex workflows
- **Eval Metrics**: TBD (relevance score? user feedback?)

---

### Phase 5: Learning Memory System 📋 PLANNED

**Goal**: Build personalized learning profile over time

**Tasks**:
- [ ] Design user preference schema
- [ ] Track topics of interest based on reading patterns
- [ ] Build knowledge graph of learned concepts
- [ ] Identify knowledge gaps and learning opportunities
- [ ] Implement recommendation engine
- [ ] Create feedback loop for preference learning

**Technical Decisions**:
- **Storage**: JSON/SQLite for user preferences?
- **Knowledge Graph**: Simple adjacency list vs. graph database?

---

### Phase 6: Attention Scoring 📋 PLANNED

**Goal**: Score newsletters by relevance and attention-worthiness

**Tasks**:
- [ ] Define attention scoring algorithm
- [ ] Factors: relevance to interests, timeliness, novelty, actionability
- [ ] Implement scoring system
- [ ] Test scoring accuracy with historical newsletters
- [ ] Create feedback mechanism to improve scoring
- [ ] Build priority queue for digest generation

---

### Phase 7: Weekly Digest Generation 📋 PLANNED

**Goal**: Automatically generate and deliver weekly digests

**Tasks**:
- [ ] Design digest format and structure
- [ ] Aggregate top insights from week's newsletters
- [ ] Generate personalized learning recommendations
- [ ] Format digest for email/web delivery
- [ ] Schedule weekly digest job
- [ ] Test digest generation end-to-end

---

### Phase 8: Evaluation Framework 📋 PLANNED

**Goal**: Build continuous eval loop for quality assurance

**Tasks**:
- [ ] Define key metrics (relevance, insight quality, user satisfaction)
- [ ] Build automated eval suite
- [ ] Create benchmark dataset
- [ ] Implement A/B testing for prompt variations
- [ ] Add user feedback collection
- [ ] Set up monitoring dashboards

**Eval Metrics**:
- Insight relevance score
- User engagement rate
- Recommendation accuracy
- Newsletter prioritization accuracy

---

### Phase 9: User Interface 📋 PLANNED

**Goal**: Build Streamlit UI for user interaction and feedback

**Tasks**:
- [ ] Design UI wireframes
- [ ] Build newsletter browsing interface
- [ ] Create digest viewing page
- [ ] Add feedback controls (thumbs up/down, relevance ratings)
- [ ] Implement preference settings page
- [ ] Add analytics dashboard
- [ ] Deploy to Replit

---

### Phase 10: Polish & Deployment 📋 PLANNED

**Goal**: Production-ready deployment

**Tasks**:
- [ ] Code cleanup and refactoring
- [ ] Comprehensive documentation
- [ ] Performance optimization
- [ ] Security audit
- [ ] Error handling and logging improvements
- [ ] Deploy to Replit (publish)
- [ ] Share with beta users

---

## Technical Stack

| Component | Technology | Status |
|-----------|-----------|--------|
| **Language** | Python 3.11 | ✅ Configured |
| **Email Source** | Gmail API (OAuth 2.0) | ✅ Integrated |
| **Testing** | pytest with mocking | ✅ Implemented |
| **Vector Storage** | FAISS | 📋 Planned |
| **LLM** | OpenAI (via Replit) | 📋 Planned |
| **Orchestration** | LangGraph/AgentKit | 📋 Planned |
| **UI** | Streamlit | 📋 Planned |
| **Deployment** | Replit Publishing | 📋 Planned |

## Development Principles

1. **Test-Driven Development**: Write tests before implementation
2. **Iterative Progress**: Ship small, working increments
3. **User-Centric**: Build for real user needs (my own newsletters first)
4. **Eval-Driven**: Measure quality continuously
5. **Learning-Focused**: Document learnings and decisions

## Success Metrics

### Short-term (Foundation)
- ✅ Successfully fetch and parse newsletters from Gmail
- ✅ 100% test coverage for core functionality
- ✅ Handle real-world newsletter formats

### Mid-term (MVP)
- [ ] Generate weekly digest from 10+ newsletters
- [ ] 80%+ insight relevance score
- [ ] Personalized recommendations based on reading history

### Long-term (Production)
- [ ] Deploy to Replit with public URL
- [ ] 5+ beta users actively using the digest
- [ ] <2% error rate in production
- [ ] Positive user feedback on learning value

## Timeline

- **Week 1-2**: Foundation ✅ COMPLETE
- **Week 3**: Newsletter Filtering 🚧 CURRENT
- **Week 4**: Content Extraction & Storage
- **Week 5-6**: AI Synthesis Pipeline
- **Week 7**: Learning Memory System
- **Week 8**: Attention Scoring & Digest Generation
- **Week 9**: Evaluation Framework
- **Week 10**: UI Development
- **Week 11**: Polish & Deployment

## Open Questions

- [ ] What's the best chunking strategy for newsletter content?
- [ ] How to measure "insight quality" objectively?
- [ ] Should we use local embeddings or OpenAI embeddings?
- [ ] What's the right balance between summary length and detail?
- [ ] How to handle newsletters in different languages?

## Resources & References

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

**Next Steps**: Implement newsletter filtering to identify newsletters specifically from the user's Gmail inbox.
