# 📰 Newsletter Digest Agent 2.0

> Your personalized AI research companion for newsletter insights

Transform newsletter overload into actionable learning insights with AI-powered synthesis, trend identification, and personalized learning prompts.

## ✨ Features

- **📧 Gmail Integration**: Automatically fetch newsletters from your inbox
- **🤖 AI Synthesis**: Extract key insights and trends using OpenAI
- **🎯 Personalized Learning**: Generate custom learning challenges based on insights
- **💾 Vector Memory**: FAISS-based storage for semantic search across newsletters
- **📊 Evaluation Framework**: Track relevance, completeness, and actionability
- **💬 Feedback Loop**: Collect engagement data to improve future digests

## 🚀 Quick Start

1. **Fetch Newsletters**: Use the sidebar to configure your search and click "Fetch & Analyze"
2. **Review Insights**: Browse AI-generated summaries, key insights, and emerging trends
3. **Get Learning Prompts**: Generate personalized challenges for topics that interest you
4. **Provide Feedback**: Help improve the system by sharing what's useful

## 🏗️ Architecture

```
/agent          - Core agent logic (Gmail, AI synthesis, memory)
/evals          - Evaluation framework and metrics
/data           - Vector store and metadata
app.py          - Streamlit web interface
```

## 🔧 Tech Stack

- **Frontend**: Streamlit
- **AI**: OpenAI via Replit AI Integrations
- **Email**: Gmail API with OAuth
- **Memory**: FAISS vector store
- **Language**: Python 3.11

## 📚 Learning Project

This is a self-guided learning project focused on:
- Designing AI-powered products
- Building evaluation frameworks
- Implementing RAG (Retrieval-Augmented Generation)
- Shipping functional AI applications

## 🔐 Privacy & Security

- Gmail connection uses OAuth with read-only permissions
- No API keys needed (uses Replit AI Integrations)
- Feedback and data stored locally

## 📈 Future Enhancements

- Advanced embeddings for better semantic search
- Attention scoring based on user engagement
- Insight graph visualization
- Privacy controls with PII detection
- Integration with Phoenix/DeepEval for advanced evals

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

---

Built with ❤️ as a learning project to master AI product development
