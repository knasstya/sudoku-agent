"""
LangGraph passes a single shared 'state' object between every node.
Each agent reads what it needs from state and returns a dict of the
fields it wants to update — LangGraph merges that into the state
before calling the next node. This is the core mental model of the
whole framework: nodes are pure functions, state is the only channel
between them.
"""
from typing import TypedDict, List


class SudokuState(TypedDict):
    grid: List[List[int]]        # current 9x9 grid, 0 = empty
    strategy: str                 # planner's current instruction to the solver
    conflicts: List[str]          # verifier's findings, empty if valid
    attempts: int                 # retry counter, prevents infinite loops
    max_attempts: int
    rejected_moves: List[str]     # moves solver tried that failed validation, so it stops repeating them
    status: str                   # "in_progress" | "solved" | "failed"
