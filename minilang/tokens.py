from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    LET = auto()
    PRINT = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    SEMICOLON = auto()
    EOF = auto()


@dataclass(frozen=True, slots=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
    value: int | None = None

    def label(self) -> str:
        if self.type is TokenType.NUMBER:
            return f"NUMBER({self.value})"
        if self.type is TokenType.IDENTIFIER:
            return f'IDENTIFIER("{self.lexeme}")'
        return self.type.name

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "type": self.type.name,
            "lexeme": self.lexeme,
            "line": self.line,
            "column": self.column,
        }
        if self.value is not None:
            result["value"] = self.value
        return result

