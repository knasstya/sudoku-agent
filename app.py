"""
Streamlit interface. Streamlit turns a Python script into a web UI
without writing HTML/JS — standard choice for ML/AI portfolio demos
because it's fast to build and free to host (Streamlit Community Cloud).
"""
import streamlit as st

from graph import run_sudoku_agent
from sudoku_core import generate_puzzle

st.set_page_config(page_title="Sudoku Agent", layout="centered")
st.title("Sudoku Multi-Agent Solver")
st.caption("Planner -> Solver -> Verifier, orchestrated with LangGraph")

difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])

if "puzzle" not in st.session_state:
    st.session_state.puzzle = generate_puzzle(difficulty)

if st.button("New puzzle"):
    st.session_state.puzzle = generate_puzzle(difficulty)
    st.session_state.pop("result", None)


def render_grid(grid):
    for row in grid:
        st.write(" ".join(str(n) if n != 0 else "." for n in row))


st.subheader("Puzzle")
render_grid(st.session_state.puzzle)

if st.button("Solve with agents"):
    with st.spinner("Agents are working..."):
        result = run_sudoku_agent(st.session_state.puzzle, max_attempts=15)
        st.session_state.result = result

if "result" in st.session_state:
    result = st.session_state.result
    st.subheader(f"Result: {result['status']} (attempts: {result['attempts']})")
    render_grid(result["grid"])
    if result["conflicts"]:
        st.warning("Remaining conflicts: " + "; ".join(result["conflicts"]))
