from typing import TypedDict


class SudokuState(TypedDict):
    grid: list[list[int]]        # current 9x9 grid, 0 = empty
    strategy: str                 # planner's current instruction to the solver
    conflicts: list[str]          # verifier's findings, empty if valid
    attempts: int                 # retry counter, prevents infinite loops
    max_attempts: int
    rejected_moves: list[str]     # moves solver tried that failed validation, so it stops repeating them
    status: str                   # "in_progress" | "solved" | "failed"
