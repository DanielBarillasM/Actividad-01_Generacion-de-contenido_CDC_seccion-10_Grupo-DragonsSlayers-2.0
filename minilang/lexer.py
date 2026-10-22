from __future__ import annotations

from .errors import MiniLangError
from .tokens import Token, TokenType


KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
}

SINGLE_CHARACTER_TOKENS = {
    "=": TokenType.EQUAL,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    ";": TokenType.SEMICOLON,
}


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.current = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []

    def scan_tokens(self) -> list[Token]:
        while not self._at_end():
            char = self._peek()
            if char in " \r\t":
                self._advance()
            elif char == "\n":
                self._advance()
                self.line += 1
                self.column = 1
            elif char == "/" and self._peek_next() == "/":
                self._skip_comment()
            elif char.isdigit():
                self._number()
            elif char.isalpha() or char == "_":
                self._identifier()
            elif char in SINGLE_CHARACTER_TOKENS:
                line, column = self.line, self.column
                lexeme = self._advance()
                self.tokens.append(
                    Token(SINGLE_CHARACTER_TOKENS[lexeme], lexeme, line, column)
                )
            else:
                raise MiniLangError(f"Caracter inesperado: {char!r}", self.line, self.column)

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _identifier(self) -> None:
        start = self.current
        line, column = self.line, self.column
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()
        lexeme = self.source[start:self.current]
        token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
        self.tokens.append(Token(token_type, lexeme, line, column))

    def _number(self) -> None:
        start = self.current
        line, column = self.line, self.column
        while self._peek().isdigit():
            self._advance()
        lexeme = self.source[start:self.current]
        value = int(lexeme)
        if value > 2_147_483_647:
            raise MiniLangError("El entero excede el rango de i32", line, column)
        self.tokens.append(Token(TokenType.NUMBER, lexeme, line, column, value))

    def _skip_comment(self) -> None:
        while not self._at_end() and self._peek() != "\n":
            self._advance()

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def _peek(self) -> str:
        return "\0" if self._at_end() else self.source[self.current]

    def _peek_next(self) -> str:
        index = self.current + 1
        return "\0" if index >= len(self.source) else self.source[index]

    def _at_end(self) -> bool:
        return self.current >= len(self.source)

