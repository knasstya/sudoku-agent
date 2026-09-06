"""
Builds the LangGraph StateGraph: this is where nodes become edges.

Flow:
  planner -> solver -> verifier -> (loop back to planner) OR (end)

The conditional edge is the part that makes this "agentic" rather
than a linear script: the graph itself decides whether to retry
based on the verifier's output, not hardcoded application logic.
"""
import time
from langgraph.graph import StateGraph, END
from agents.state import SudokuState
from agents.planner import planner_node
from agents.solver import solver_node
from agents.verifier import verifier_node


def _route_after_verify(state: SudokuState) -> str:
    if state["status"] in ("solved", "failed"):
        return END

    time.sleep(15)  # stay under Groq free-tier rate limit before the next round
    return "planner"


def build_graph():
    graph = StateGraph(SudokuState)

    graph.add_node("planner", planner_node)
    graph.add_node("solver", solver_node)
    graph.add_node("verifier", verifier_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "solver")
    graph.add_edge("solver", "verifier")
    graph.add_conditional_edges("verifier", _route_after_verify, {
        "planner": "planner",
        END: END,
    })

    return graph.compile()


def run_sudoku_agent(initial_grid, max_attempts: int = 8) -> SudokuState:
    app = build_graph()
    initial_state: SudokuState = {
        "grid": initial_grid,
        "strategy": "",
        "conflicts": [],
        "attempts": 0,
        "max_attempts": max_attempts,
        "rejected_moves": [],
        "status": "in_progress",
    }
    return app.invoke(initial_state)
