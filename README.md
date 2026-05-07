# AI-QA-Agent

An AI-assisted QA Agent prototype for generating test cases, analyzing failures, and demonstrating the architecture of an autonomous QA platform.

## Overview

AI-QA-Agent combines a FastAPI backend, a Next.js dashboard, reusable agent classes, prompt templates, and automation runner scaffolding. The current implementation is intentionally interview-friendly: the test generation and bug analysis agents run with deterministic mock LLM responses, while the architecture leaves clear extension points for real LLM providers, vector search, Playwright execution, and analytics.

## Features

### Core Capabilities
- **Test Case Generator**: Generates structured test cases from user stories, PRDs, and API-style inputs
- **Bug Analysis Agent**: Produces root-cause summaries and remediation suggestions from failure data
- **Automation Runner Scaffolding**: Playwright and API runner modules with self-healing and contract-testing extension points
- **Analytics Dashboard**: Frontend dashboard for QA metrics and agent workflows
- **FastAPI Backend**: Versioned API routes for health checks, agents, generation, execution, and analytics

### Advanced Features
- Deterministic mock agent responses for local demos without API keys
- Clear LLM provider abstraction points for OpenAI/LangChain integration
- Async service layer and SQLAlchemy models for generated tests and agent executions
- Docker Compose setup for PostgreSQL, Redis, ChromaDB, backend, and frontend

## Architecture

The platform follows clean architecture principles with domain-driven design:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: External dependencies (DB, LLM, etc.)
- **Presentation Layer**: APIs and UI

### Key Components
- `agents/`: AI agent implementations
- `prompts/`: LLM prompt templates
- `automation/`: UI and API test execution runner scaffolding
- `backend/`: FastAPI application, schemas, services, and models
- `frontend/`: Next.js dashboard

## Tech Stack

### Frontend
- Next.js 14
- TypeScript
- TailwindCSS
- React Query

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- Pydantic

### AI/LLM
- OpenAI SDK
- LangChain
- ChromaDB
- Custom prompt engineering

### Automation
- Playwright
- Pytest
- Requests/httpx

### Infrastructure
- PostgreSQL
- Redis
- Docker
- OpenTelemetry
- Prometheus

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 20+

### Setup

1. Clone the repository
```bash
git clone https://github.com/srinivasansakthivel/qa-agent.git
cd qa-agent
```

2. Start the stack with Docker
```bash
docker compose up -d
```

Or run services locally:

3. Install backend dependencies
```bash
python -m pip install -r backend/requirements.txt
```

4. Install frontend dependencies
```bash
cd frontend
npm install
```

5. Start the backend
```bash
cd ..
export PYTHONPATH=backend:.
uvicorn app.main:app --reload
```

6. Start the frontend
```bash
cd frontend
npm run dev
```

## Documentation

- [System Design](docs/system_design.md)
- [AI Engineering Review](docs/AI_ENGINEERING_REVIEW.md)

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Development

### Code Quality
- **Linting**: ruff, eslint
- **Formatting**: black, prettier
- **Type Checking**: mypy
- **Testing**: pytest, jest

### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

### Running Tests
```bash
# Backend import/compile smoke checks
python -m compileall -q backend agents automation prompts
PYTHONPATH=backend:. python -c "from app.main import app; print(app.title)"

# Frontend checks
cd frontend && npm run type-check && npm run build
```

## Deployment

### Docker
Use `docker compose up -d` for the local multi-service stack.

### CI/CD
GitHub Actions workflows are configured for automated testing and deployment.

## Interview Walkthrough Notes

This project demonstrates:

1. **Architecture**: FastAPI service boundaries, SQLAlchemy models, agent abstractions, and prompt modules
2. **AI Engineering Thinking**: Mocked local agents with clear provider integration points
3. **QA Domain Coverage**: Test generation, bug analysis, UI/API runner scaffolding, and analytics
4. **Pragmatism**: Local demo works without paid LLM credentials, while still documenting production trade-offs
5. **Modern Practices**: TypeScript frontend, Dockerized services, CI smoke checks

### Key Discussion Points
- Trade-offs between different AI approaches
- Cost optimization for LLM calls
- Security considerations for AI agents
- Scalability challenges and solutions

## Future Roadmap

- Multi-modal test generation (video, audio)
- Integration with popular CI/CD platforms
- Advanced ML models for test prediction
- Real-time collaborative testing
- Plugin marketplace

## Trade-offs and Limitations

### Performance vs Accuracy
- LLM calls introduce latency; caching and batching help
- Self-healing locators may occasionally misidentify elements

### Cost Considerations
- LLM API costs scale with usage; implement rate limiting and caching
- Vector database storage grows with test history

### Security
- AI agents require careful prompt sanitization
- Test data generation must avoid PII exposure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
