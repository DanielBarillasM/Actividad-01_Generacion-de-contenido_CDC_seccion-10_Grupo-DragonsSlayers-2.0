from __future__ import annotations


class MiniLangError(Exception):
    """Error con ubicacion precisa dentro del programa fuente."""

    def __init__(self, message: str, line: int, column: int) -> None:
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Linea {line}, columna {column}: {message}")

