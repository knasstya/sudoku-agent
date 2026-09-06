"""
Solver agent: fills cells via pure logic where possible (free, 100%
reliable), asks the LLM only for genuinely ambiguous cells, and falls
back to a deterministic backtracking solver if the LLM can't make
progress -- guaranteeing the puzzle actually finishes.
"""
import json
import re

from langchain_core.messages import HumanMessage, SystemMessage

from sudoku_core import _is_valid_placement, _solve, find_naked_singles

from .llm_client import get_llm
from .state import SudokuState

SYSTEM_PROMPT = """You are a Sudoku solver. Given a grid and a strategy hint,
propose moves as a JSON array only, no other text. Each move:
{"row": 0-8, "col": 0-8, "value": 1-9}
Only propose a move if you are certain it is correct. Propose at most 5 moves.
Only fill currently empty (0) cells."""


def _extract_json(text: str) -> list:
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        return []
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return []


def solver_node(state: SudokuState) -> dict:
    grid = [row[:] for row in state["grid"]]

    singles = find_naked_singles(grid)
    if singles:
        applied = 0
        for r, c, v in singles:
            if grid[r][c] == 0 and _is_valid_placement(grid, r, c, v):
                grid[r][c] = v
                applied += 1
        print(f"[Solver] Filled {applied} cell(s) via pure logic (naked singles), no LLM call needed")
        return {"grid": grid, "attempts": state["attempts"] + 1, "rejected_moves": state["rejected_moves"]}

    print("[Solver] No naked singles left, asking LLM for a harder move...")
    llm = get_llm()
    grid_str = "\n".join(" ".join(str(n) for n in row) for row in grid)
    rejected_note = (
        f"\n\nThese exact moves were already tried and are WRONG, do not repeat them: {state['rejected_moves']}"
        if state["rejected_moves"] else ""
    )

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Strategy: {state['strategy']}\n\nGrid:\n{grid_str}{rejected_note}"),
    ])
    print(f"[Solver] Raw response: {response.content[:150]}")

    moves = _extract_json(response.content)
    print(f"[Solver] Parsed {len(moves)} candidate move(s)")

    applied = 0
    rejected = list(state["rejected_moves"])
    for move in moves:
        try:
            r, c, v = int(move["row"]), int(move["col"]), int(move["value"])
        except (KeyError, ValueError, TypeError):
            continue
        if not (0 <= r < 9 and 0 <= c < 9 and 1 <= v <= 9):
            continue
        if grid[r][c] != 0:
            continue
        if _is_valid_placement(grid, r, c, v):
            grid[r][c] = v
            applied += 1
        else:
            rejected.append(f"row {r}, col {c}, value {v}")

    print(f"[Solver] Applied {applied} valid move(s) to the grid")

    if applied == 0:
        print("[Solver] LLM made no progress on a hard cell — completing deterministically")
        _solve(grid)

    return {"grid": grid, "attempts": state["attempts"] + 1, "rejected_moves": rejected}