from __future__ import annotations

from .ast_nodes import Binary, Expression, LetStatement, Number, PrintStatement, Program, Unary


def optimize_program(program: Program) -> Program:
    statements = []
    for statement in program.statements:
        if isinstance(statement, LetStatement):
            statements.append(
                LetStatement(
                    statement.name,
                    fold_constants(statement.initializer),
                    statement.line,
                    statement.column,
                )
            )
        elif isinstance(statement, PrintStatement):
            statements.append(
                PrintStatement(
                    fold_constants(statement.expression),
                    statement.line,
                    statement.column,
                )
            )
    return Program(tuple(statements))


def fold_constants(expression: Expression) -> Expression:
    if isinstance(expression, Unary):
        operand = fold_constants(expression.operand)
        if expression.operator == "-" and isinstance(operand, Number):
            return Number(-operand.value, expression.line, expression.column)
        return Unary(expression.operator, operand, expression.line, expression.column)

    if isinstance(expression, Binary):
        left = fold_constants(expression.left)
        right = fold_constants(expression.right)
        if isinstance(left, Number) and isinstance(right, Number):
            if expression.operator == "+":
                value = left.value + right.value
            elif expression.operator == "-":
                value = left.value - right.value
            elif expression.operator == "*":
                value = left.value * right.value
            elif expression.operator == "/" and right.value != 0:
                value = int(left.value / right.value)
            else:
                return Binary(left, expression.operator, right, expression.line, expression.column)
            if -(2**31) <= value <= 2**31 - 1:
                return Number(value, expression.line, expression.column)
        return Binary(left, expression.operator, right, expression.line, expression.column)

    return expression

