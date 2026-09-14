"""
Verifier agent: deliberately NOT an LLM call. Rule-checking is
deterministic, so using an LLM here would be slower, costlier and
less reliable than plain code for no benefit.
"""
from sudoku_core import find_conflicts, is_valid_solution

from .state import SudokuState


def verifier_node(state: SudokuState) -> dict:
    grid = state["grid"]
    is_full = all(cell != 0 for row in grid for cell in row)

    if is_full and is_valid_solution(grid):
        print("[Verifier] Solved!")
        return {"status": "solved", "conflicts": []}

    conflicts = find_conflicts(grid)
    empty_count = sum(row.count(0) for row in grid)
    print(f"[Verifier] Not solved yet — {empty_count} empty cells, {len(conflicts)} conflict(s)")

    if state["attempts"] >= state["max_attempts"]:
        print("[Verifier] Max attempts reached, stopping.")
        return {"status": "failed", "conflicts": conflicts}

    return {"status": "in_progress", "conflicts": conflicts}
