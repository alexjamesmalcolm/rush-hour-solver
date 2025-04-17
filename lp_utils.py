from typing import List, Optional, Tuple
from pulp import LpProblem, LpVariable, LpAffineExpression


def lp_and(
    a: LpVariable, b: LpVariable, answer: LpVariable, definition: Optional[str] = None
) -> List[LpAffineExpression | Tuple[LpAffineExpression, str]]:
    """Logical AND that I borrowed from: https://cs.stackexchange.com/a/12118"""
    constraints: List[Tuple[LpAffineExpression, str]] = [
        (answer >= a + b - 1, f"{definition}__first_and"),
        (answer <= a, f"{definition}__second_and"),
        (answer <= b, f"{definition}__third_and"),
    ]
    if not definition:
        return [constraint for constraint, _ in constraints]
    return constraints


def lp_or(
    a: LpVariable, b: LpVariable, answer: LpVariable, definition: Optional[str] = None
) -> List[LpAffineExpression | Tuple[LpAffineExpression, str]]:
    """Logical OR (not XOR) that I borrowed from: https://cs.stackexchange.com/a/12118"""
    constraints: List[Tuple[LpAffineExpression, str]] = [
        (answer <= a + b, f"{definition}__first_or"),
        (answer >= a, f"{definition}__second_or"),
        (answer >= b, f"{definition}__third_or"),
    ]
    if not definition:
        return [constraint for constraint, _ in constraints]
    return constraints


def lp_xor(
    a: LpVariable, b: LpVariable, answer: LpVariable, definition: Optional[str] = None
) -> List[LpAffineExpression | Tuple[LpAffineExpression, str]]:
    """Logical XOR (not OR) that I borrowed from: https://cs.stackexchange.com/a/12118"""
    constraints: List[Tuple[LpAffineExpression, str]] = [
        (answer <= a + b, f"{definition}__first_xor"),
        (answer >= a - b, f"{definition}__second_xor"),
        (answer >= b - a, f"{definition}__third_xor"),
        (answer <= 2 - a - b, f"{definition}__fourth_xor"),
    ]
    if not definition:
        return [constraint for constraint, _ in constraints]
    return constraints


def add_constraints(
    problem: LpProblem,
    constraints: List[LpAffineExpression | Tuple[LpAffineExpression, str]],
) -> LpProblem:
    """A method for quickly adding constraints, can be used in conjunction with other logical
    constraint generators."""
    for c in constraints:
        problem += c
    return problem
