from __future__ import annotations

from .ast_nodes import Binary, Expression, Identifier, LetStatement, Number, PrintStatement, Program, Unary
from .semantic import Symbol


WASM_OPERATORS = {
    "+": "i32.add",
    "-": "i32.sub",
    "*": "i32.mul",
    "/": "i32.div_s",
}


class WatGenerator:
    def __init__(self, symbols: tuple[Symbol, ...]) -> None:
        self.symbols = {symbol.name: symbol for symbol in symbols}
        self.lines: list[str] = []

    def generate(self, program: Program) -> str:
        self.lines = [
            "(module",
            '  (import "env" "print_i32" (func $print_i32 (param i32)))',
            '  (func (export "main")',
        ]
        for symbol in self.symbols.values():
            self.lines.append(f"    (local ${symbol.name} i32)")

        if self.symbols:
            self.lines.append("")

        for statement in program.statements:
            if isinstance(statement, LetStatement):
                self._expression(statement.initializer)
                self.lines.append(f"    local.set ${statement.name}")
            elif isinstance(statement, PrintStatement):
                self._expression(statement.expression)
                self.lines.append("    call $print_i32")

        self.lines.extend(["  )", ")"])
        return "\n".join(self.lines) + "\n"

    def _expression(self, expression: Expression) -> None:
        if isinstance(expression, Number):
            self.lines.append(f"    i32.const {expression.value}")
        elif isinstance(expression, Identifier):
            self.lines.append(f"    local.get ${expression.name}")
        elif isinstance(expression, Unary):
            self.lines.append("    i32.const 0")
            self._expression(expression.operand)
            self.lines.append("    i32.sub")
        elif isinstance(expression, Binary):
            self._expression(expression.left)
            self._expression(expression.right)
            self.lines.append(f"    {WASM_OPERATORS[expression.operator]}")
        else:
            raise TypeError(f"Expresion no soportada: {type(expression).__name__}")

