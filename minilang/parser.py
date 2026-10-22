from __future__ import annotations

from .ast_nodes import Binary, Expression, Identifier, LetStatement, Number, PrintStatement, Program, Statement, Unary
from .errors import MiniLangError
from .tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements: list[Statement] = []
        while not self._check(TokenType.EOF):
            statements.append(self._statement())
        return Program(tuple(statements))

    def _statement(self) -> Statement:
        if self._match(TokenType.LET):
            return self._let_statement(self._previous())
        if self._match(TokenType.PRINT):
            return self._print_statement(self._previous())
        token = self._peek()
        raise MiniLangError("Se esperaba 'let' o 'print'", token.line, token.column)

    def _let_statement(self, keyword: Token) -> LetStatement:
        name = self._expect(TokenType.IDENTIFIER, "Se esperaba un nombre de variable")
        self._expect(TokenType.EQUAL, "Se esperaba '=' despues del identificador")
        initializer = self._expression()
        self._expect(TokenType.SEMICOLON, "Se esperaba ';' al final de la declaracion")
        return LetStatement(name.lexeme, initializer, keyword.line, keyword.column)

    def _print_statement(self, keyword: Token) -> PrintStatement:
        self._expect(TokenType.LEFT_PAREN, "Se esperaba '(' despues de 'print'")
        expression = self._expression()
        self._expect(TokenType.RIGHT_PAREN, "Se esperaba ')' despues de la expresion")
        self._expect(TokenType.SEMICOLON, "Se esperaba ';' al final de print")
        return PrintStatement(expression, keyword.line, keyword.column)

    def _expression(self) -> Expression:
        return self._addition()

    def _addition(self) -> Expression:
        expression = self._multiplication()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self._multiplication()
            expression = Binary(expression, operator.lexeme, right, operator.line, operator.column)
        return expression

    def _multiplication(self) -> Expression:
        expression = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous()
            right = self._unary()
            expression = Binary(expression, operator.lexeme, right, operator.line, operator.column)
        return expression

    def _unary(self) -> Expression:
        if self._match(TokenType.MINUS):
            operator = self._previous()
            return Unary(operator.lexeme, self._unary(), operator.line, operator.column)
        return self._primary()

    def _primary(self) -> Expression:
        if self._match(TokenType.NUMBER):
            token = self._previous()
            assert token.value is not None
            return Number(token.value, token.line, token.column)
        if self._match(TokenType.IDENTIFIER):
            token = self._previous()
            return Identifier(token.lexeme, token.line, token.column)
        if self._match(TokenType.LEFT_PAREN):
            expression = self._expression()
            self._expect(TokenType.RIGHT_PAREN, "Se esperaba ')' para cerrar la expresion")
            return expression
        token = self._peek()
        raise MiniLangError("Se esperaba un numero, identificador o parentesis", token.line, token.column)

    def _match(self, *types: TokenType) -> bool:
        if any(self._check(token_type) for token_type in types):
            self._advance()
            return True
        return False

    def _expect(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        token = self._peek()
        raise MiniLangError(message, token.line, token.column)

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type is token_type

    def _advance(self) -> Token:
        if not self._check(TokenType.EOF):
            self.current += 1
        return self._previous()

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

