from typing import List, Optional, Tuple
from pulp import LpProblem, LpVariable, LpAffineExpression


def lp_and(
    a: LpVariable, b: LpVariable, answer: LpVariable, name: Optional[str] = None
) -> List[LpAffineExpression | Tuple[LpAffineExpression, str]]:
    """Logical AND that I borrowed from: https://cs.stackexchange.com/a/12118"""
    constraints: List[Tuple[LpAffineExpression, str]] = [
        (answer >= a + b - 1, f"{name}__first_and"),
        (answer <= a, f"{name}__second_and"),
        (answer <= b, f"{name}__third_and"),
    ]
    if not name:
        return [constraint for constraint, _ in constraints]
    return constraints


def lp_or(
    a: LpVariable, b: LpVariable, answer: LpVariable, name: Optional[str] = None
) -> List[LpAffineExpression | Tuple[LpAffineExpression, str]]:
    """Logical OR (not XOR) that I borrowed from: https://cs.stackexchange.com/a/12118"""
    constraints: List[Tuple[LpAffineExpression, str]] = [
        (answer <= a + b, f"{name}__first_or"),
        (answer >= a, f"{name}__second_or"),
        (answer >= b, f"{name}__third_or"),
    ]
    if not name:
        return [constraint for constraint, _ in constraints]
    return constraints


def lp_xor(
    a: LpVariable, b: LpVariable, answer: LpVariable, name: Optional[str] = None
) -> List[LpAffineExpression | Tuple[LpAffineExpression, str]]:
    """Logical XOR (not OR) that I borrowed from: https://cs.stackexchange.com/a/12118"""
    constraints: List[Tuple[LpAffineExpression, str]] = [
        (answer <= a + b, f"{name}__first_xor"),
        (answer >= a - b, f"{name}__second_xor"),
        (answer >= b - a, f"{name}__third_xor"),
        (answer <= 2 - a - b, f"{name}__fourth_xor"),
    ]
    if not name:
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
