"""Calculator tool — safe math expression evaluator."""

from langchain_classic.agents import Tool


def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    allowed = set("0123456789+-*/.() ")
    if not all(ch in allowed for ch in expression):
        return "Error: Only numeric math expressions are supported."
    try:
        result = eval(expression)   # safe: filtered to digits & operators
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


def get_calculator_tool() -> Tool:
    """Return a LangChain Tool wrapping the calculator."""
    return Tool(
        name="Calculator",
        func=calculator,
        description=(
            "Evaluate a mathematical expression. "
            "Input should be a valid math expression like '245 * 18 + 32'."
        ),
    )
