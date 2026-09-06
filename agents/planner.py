"""
Planner agent: looks at the grid (and any conflicts from a previous
failed attempt) and produces a short strategy instruction for the
Solver. On the first pass this is generic; on retries it reacts
specifically to what went wrong, which is what makes the loop useful
instead of just retrying blindly.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from .llm_client import get_llm
from .state import SudokuState

SYSTEM_PROMPT = """You are a Sudoku strategy planner. You do not solve the
puzzle yourself. You output ONE short instruction (max 2 sentences) telling
a solver agent which technique or region to focus on next.
Common techniques: naked singles, hidden singles, scanning rows/columns/boxes
with the fewest empty cells first, elimination by box.
If given a list of conflicts from a previous attempt, prioritize fixing
those specific regions."""


def planner_node(state: SudokuState) -> dict:
    print(f"[Planner] Round {state['attempts'] + 1} — thinking about strategy...")
    llm = get_llm()

    conflict_note = (
        f"Previous attempt had these conflicts, fix these regions first: {state['conflicts']}"
        if state["conflicts"]
        else "This is the first attempt."
    )

    grid_str = "\n".join(" ".join(str(n) for n in row) for row in state["grid"])

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Grid (0 = empty):\n{grid_str}\n\n{conflict_note}"),
    ])

    print(f"[Planner] Strategy: {response.content[:100]}")
    return {"strategy": response.content}
