"""
Core Sudoku logic: generation and rule validation.
No LLM involved here on purpose — agents should reason on TOP of
ground-truth rules, not reinvent them. This file is the "data" layer.
"""
import random
from typing import List, Optional

Grid = List[List[int]]  # 9x9, 0 = empty cell


def _is_valid_placement(grid: Grid, row: int, col: int, num: int) -> bool:
    if num in grid[row]:
        return False
    if num in [grid[r][col] for r in range(9)]:
        return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num:
                return False
    return True


def _solve(grid: Grid) -> bool:
    """Backtracking solver, used internally to generate valid full grids."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if _is_valid_placement(grid, row, col, num):
                        grid[row][col] = num
                        if _solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True


def generate_full_solution() -> Grid:
    grid = [[0] * 9 for _ in range(9)]
    _solve(grid)
    return grid


def generate_puzzle(difficulty: str = "easy") -> Grid:
    """
    Removes cells from a full solution to create a puzzle.
    difficulty controls how many cells are blanked out.
    """
    holes = {"easy": 35, "medium": 45, "hard": 55}.get(difficulty, 35)
    solution = generate_full_solution()
    puzzle = [row[:] for row in solution]

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:holes]:
        puzzle[r][c] = 0
    return puzzle


def is_valid_solution(grid: Grid) -> bool:
    """Checks full 9x9 grid against Sudoku rules. Returns False on any
    empty cell (0) too, since an incomplete grid isn't a valid solution."""
    for row in grid:
        if sorted(row) != list(range(1, 10)):
            return False
    for col in range(9):
        if sorted(grid[r][col] for r in range(9)) != list(range(1, 10)):
            return False
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = [
                grid[r][c]
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
            ]
            if sorted(box) != list(range(1, 10)):
                return False
    return True

def get_candidates(grid: Grid, row: int, col: int) -> set:
    """Returns the set of numbers that could legally go in this cell
    right now, based on its row/column/box. Empty set if cell is filled."""
    if grid[row][col] != 0:
        return set()
    used = set(grid[row]) | {grid[r][col] for r in range(9)}
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    used |= {
        grid[r][c]
        for r in range(box_row, box_row + 3)
        for c in range(box_col, box_col + 3)
    }
    return set(range(1, 10)) - used


def find_naked_singles(grid: Grid) -> List[tuple]:
    """Finds cells that have exactly ONE possible legal value — these
    can be filled with certainty by pure logic, no LLM reasoning needed.
    Returns a list of (row, col, value) tuples."""
    singles = []
    for r in range(9):
        for c in range(9):
            candidates = get_candidates(grid, r, c)
            if len(candidates) == 1:
                singles.append((r, c, next(iter(candidates))))
    return singles


def find_conflicts(grid: Grid) -> List[str]:
    """Returns human-readable list of rule violations. Empty list = valid.
    Used by the Verifier agent to give the Planner agent something
    specific to react to, instead of a plain pass/fail."""
    conflicts = []
    for i, row in enumerate(grid):
        filled = [n for n in row if n != 0]
        if len(filled) != len(set(filled)):
            conflicts.append(f"Row {i} has a duplicate number")
    for c in range(9):
        col_vals = [grid[r][c] for r in range(9) if grid[r][c] != 0]
        if len(col_vals) != len(set(col_vals)):
            conflicts.append(f"Column {c} has a duplicate number")
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_vals = [
                grid[r][c]
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
                if grid[r][c] != 0
            ]
            if len(box_vals) != len(set(box_vals)):
                conflicts.append(f"Box at ({box_row},{box_col}) has a duplicate number")
    return conflicts
