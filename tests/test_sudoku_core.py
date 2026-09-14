import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku_core import (
    find_conflicts,
    generate_full_solution,
    generate_puzzle,
    is_valid_solution,
)


def test_generate_full_solution_is_valid():
    solution = generate_full_solution()
    assert is_valid_solution(solution)


def test_generate_puzzle_has_correct_hole_count():
    puzzle = generate_puzzle("easy")
    empty_cells = sum(row.count(0) for row in puzzle)
    assert empty_cells == 35


def test_generate_puzzle_difficulty_levels():
    easy = sum(row.count(0) for row in generate_puzzle("easy"))
    hard = sum(row.count(0) for row in generate_puzzle("hard"))
    assert hard > easy


def test_valid_solution_detects_duplicate_row():
    grid = generate_full_solution()
    grid[0][1] = grid[0][0]  # force a duplicate in row 0
    assert is_valid_solution(grid) is False


def test_incomplete_grid_is_not_valid():
    grid = [[0] * 9 for _ in range(9)]
    assert is_valid_solution(grid) is False


def test_find_conflicts_empty_grid_has_none():
    grid = [[0] * 9 for _ in range(9)]
    assert find_conflicts(grid) == []


def test_find_conflicts_detects_column_duplicate():
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 5
    grid[1][0] = 5
    conflicts = find_conflicts(grid)
    assert any("Column 0" in c for c in conflicts)


def test_find_conflicts_detects_box_duplicate():
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 7
    grid[1][1] = 7
    conflicts = find_conflicts(grid)
    assert any("Box at (0,0)" in c for c in conflicts)
