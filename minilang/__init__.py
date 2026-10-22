"""MiniLang: un compilador educativo hacia WebAssembly."""

from .compiler import CompilationResult, compile_source, execute_wat
from .errors import MiniLangError

__all__ = ["CompilationResult", "MiniLangError", "compile_source", "execute_wat"]

