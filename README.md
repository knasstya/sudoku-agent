# Sudoku Multi-Agent Solver

A multi-agent system that solves Sudoku puzzles through three
LLM-orchestrated agents built with **LangGraph**, with a self-correcting
retry loop and a deterministic rule layer underneath.

## Why this project

Built to demonstrate agentic pipeline design end-to-end: puzzle generation
(ETL-equivalent) -> agent orchestration (LangGraph) -> LLM reasoning calls
(Groq/Llama) -> tested, verifiable output -> deployable interface (Streamlit).

## Architecture

```
generate_puzzle()
      |
      v
  [Planner] --analyzes grid, picks a strategy--
      |
      v
  [Solver] --proposes moves, validated against rules before applying--
      |
      v
  [Verifier] --checks Sudoku rules (no LLM call, pure logic)--
      |
      +--invalid, attempts left--> back to [Planner]
      |
      +--valid or out of attempts--> END
```

Design decisions worth noting:
- **Verifier is not an LLM call.** Rule-checking is deterministic; using an
  LLM there would add cost and unreliability for no benefit.
- **Solver moves are re-validated in code**, never trusted blindly from the
  LLM output. The model proposes, deterministic code disposes.
- **CI tests only the deterministic layer** (`sudoku_core.py`), so the
  pipeline never needs an API key as a GitHub secret and costs nothing to
  run on every push.

## Stack

- LangGraph — agent orchestration / state graph
- Groq API (Llama 3.3 70B) — free-tier LLM inference
- Streamlit — interface
- pytest + GitHub Actions — testing and CI

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your Groq key
```

Get a free Groq API key at https://console.groq.com (no card required).

## Run

```bash
streamlit run app.py
```

## Test

```bash
pytest tests/test_sudoku_core.py -v
```

## Roadmap / stretch goals

- [ ] Deploy on Azure Functions / Container Apps
- [ ] Add deploy step to GitHub Actions (test -> build -> deploy)
- [ ] Swap Groq for local Ollama as a provider-agnostic demo
