# LangGraph Deep Dive Tutorial

## Project Overview
A comprehensive 3-hour hands-on tutorial designed to teach the fundamentals of LangGraph, a library for building stateful, multi-actor applications with LLMs. The tutorial focuses on practical, hands-on learning through progressive exercises.

## Prerequisites
- Python programming experience
- Basic understanding of LLMs and API interactions
- No prior LangChain experience required
- Python 3.13 environment

## Required APIs/Tools
- OpenAI API key for LLM interactions
- UV for environment management
- Ruff for code formatting and linting

## Environment Setup

This project uses environment variables for configuration. To set up:

1. Copy `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and fill in your API keys:
   - OPENAI_API_KEY: Your OpenAI API key
   - TAVILY_API_KEY: Your Tavily API key
   - Optional: LANGSMITH_API_KEY and other configuration

3. The `.env` file is ignored by git to keep your keys secure

## Project Structure
```
.
├── .DS_Store
├── .env.template
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── pyproject.toml
├── solutions
│   ├── .DS_Store
│   ├── unit1
│   │   ├── .DS_Store
│   │   └── __init__.py
│   └── unit2
│       ├── .DS_Store
│       └── __init__.py
├── src
│   ├── .DS_Store
│   ├── __init__.py
│   ├── config.py
│   └── exercises
│       ├── .DS_Store
│       ├── __init__.py
│       ├── unit1
│       │   ├── __init__.py
│       │   ├── exercise1.py
│       │   ├── exercise2.py
│       │   └── exercise3.py
│       └── unit2
│           ├── __init__.py
│           ├── exercise1.py
│           ├── exercise2.py
│           └── exercise3.py
└── tests
    ├── .DS_Store
    ├── __init__.py
    ├── conftest.py
    ├── test_unit1
    │   ├── .DS_Store
    │   ├── __init__.py
    │   ├── test_exercise1.py
    │   ├── test_exercise2.py
    │   └── test_exercise3.py
    └── test_unit2
        ├── .DS_Store
        ├── __init__.py
        ├── test_exercise1.py
        ├── test_exercise2.py
        └── test_exercise3.py

```

## Development Workflow
1. Environment Setup:
   ```bash
   make setup  # Creates venv and installs dependencies
   ```

2. Development:
   ```bash
   make format  # Format code
   make lint    # Check style
   make test    # Run tests
   ```

3. Testing:
   - Unit tests for exercise validation
   - Integration tests with real APIs
   - Mocked tests for development