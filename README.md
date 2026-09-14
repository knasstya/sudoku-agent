# Sudoku Multi-Agent Solver

A multi-agent system that solves Sudoku puzzles through LLM-orchestrated agents built with LangGraph, featuring a self-correcting retry loop and a deterministic rule-checking layer, with a Streamlit interface and automated tests.

## Features

- Multi-agent pipeline: Planner, Solver, and Verifier agents
- Self-correcting retry loop when a proposed solution fails validation
- Deterministic Verifier — rule-checking is pure logic, not an LLM call
- Solver moves re-validated in code before being applied
- Streamlit interface for interactive puzzle solving
- Pytest test suite covering the deterministic solving logic
- GitHub Actions CI — tests only the deterministic layer, so no API key is needed in CI

## Tech Stack

**Agent orchestration:** LangGraph
**LLM inference:** Groq API (Llama 3.3 70B, free tier)
**Interface:** Streamlit
**Testing / CI:** Pytest, GitHub Actions

## Project Structure

```
agents/            # Planner, Solver, Verifier agent logic
tests/              # Pytest test suite
.github/workflows/  # CI pipeline
app.py              # Streamlit app entry point
graph.py            # LangGraph orchestration
sudoku_core.py       # Deterministic Sudoku logic (generation, rule-checking)
requirements.txt
.env.example
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your Groq API key
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
pytest tests/test_sudoku_core.py -v
```

## Status

Core multi-agent pipeline, deterministic verification, and CI are complete and tested. Deployment and provider-agnostic support (e.g. local LLMs) are potential next steps.
