from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class Number:
    value: int
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class Identifier:
    name: str
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class Unary:
    operator: str
    operand: Expression
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class Binary:
    left: Expression
    operator: str
    right: Expression
    line: int
    column: int


Expression: TypeAlias = Number | Identifier | Unary | Binary


@dataclass(frozen=True, slots=True)
class LetStatement:
    name: str
    initializer: Expression
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class PrintStatement:
    expression: Expression
    line: int
    column: int


Statement: TypeAlias = LetStatement | PrintStatement


@dataclass(frozen=True, slots=True)
class Program:
    statements: tuple[Statement, ...]


def ast_to_dict(node: object) -> object:
    if isinstance(node, Program):
        return {
            "type": "Program",
            "statements": [ast_to_dict(statement) for statement in node.statements],
        }
    if isinstance(node, LetStatement):
        return {
            "type": "LetStatement",
            "name": node.name,
            "initializer": ast_to_dict(node.initializer),
        }
    if isinstance(node, PrintStatement):
        return {"type": "PrintStatement", "expression": ast_to_dict(node.expression)}
    if isinstance(node, Binary):
        return {
            "type": "BinaryExpression",
            "operator": node.operator,
            "left": ast_to_dict(node.left),
            "right": ast_to_dict(node.right),
        }
    if isinstance(node, Unary):
        return {
            "type": "UnaryExpression",
            "operator": node.operator,
            "operand": ast_to_dict(node.operand),
        }
    if isinstance(node, Identifier):
        return {"type": "Identifier", "name": node.name}
    if isinstance(node, Number):
        return {"type": "NumberLiteral", "value": node.value}
    raise TypeError(f"Nodo AST no soportado: {type(node).__name__}")

