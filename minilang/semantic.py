from __future__ import annotations

from dataclasses import dataclass

from .ast_nodes import Binary, Expression, Identifier, LetStatement, Number, PrintStatement, Program, Unary
from .errors import MiniLangError


@dataclass(frozen=True, slots=True)
class Symbol:
    name: str
    wasm_type: str
    local_index: int

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "type": self.wasm_type, "localIndex": self.local_index}


class SemanticAnalyzer:
    def __init__(self) -> None:
        self.symbols: dict[str, Symbol] = {}

    def analyze(self, program: Program) -> tuple[Symbol, ...]:
        for statement in program.statements:
            if isinstance(statement, LetStatement):
                if statement.name in self.symbols:
                    raise MiniLangError(
                        f"La variable '{statement.name}' ya fue declarada",
                        statement.line,
                        statement.column,
                    )
                self._check_expression(statement.initializer)
                self.symbols[statement.name] = Symbol(
                    statement.name, "i32", len(self.symbols)
                )
            elif isinstance(statement, PrintStatement):
                self._check_expression(statement.expression)
        return tuple(self.symbols.values())

    def _check_expression(self, expression: Expression) -> None:
        if isinstance(expression, Number):
            return
        if isinstance(expression, Identifier):
            if expression.name not in self.symbols:
                raise MiniLangError(
                    f"La variable '{expression.name}' no fue declarada",
                    expression.line,
                    expression.column,
                )
            return
        if isinstance(expression, Unary):
            self._check_expression(expression.operand)
            return
        if isinstance(expression, Binary):
            self._check_expression(expression.left)
            self._check_expression(expression.right)
            return
        raise TypeError(f"Expresion no soportada: {type(expression).__name__}")

