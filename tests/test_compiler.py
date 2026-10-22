from __future__ import annotations

import pytest

from minilang import MiniLangError, compile_source, execute_wat
from minilang.ast_nodes import Binary, LetStatement, Number


def test_compiles_and_executes_demo() -> None:
    result = compile_source("let resultado = 6 * 7; print(resultado);")
    assert "i32.mul" in result.wat
    assert execute_wat(result.wat) == [42]


def test_operator_precedence() -> None:
    result = compile_source("let valor = 6 + 7 * 2; print(valor);")
    declaration = result.ast.statements[0]
    assert isinstance(declaration, LetStatement)
    assert isinstance(declaration.initializer, Binary)
    assert declaration.initializer.operator == "+"
    assert execute_wat(result.wat) == [20]


def test_constant_folding() -> None:
    result = compile_source("let resultado = 6 * 7; print(resultado);", optimize=True)
    declaration = result.optimized_ast.statements[0]
    assert isinstance(declaration, LetStatement)
    assert isinstance(declaration.initializer, Number)
    assert declaration.initializer.value == 42
    assert "i32.mul" not in result.wat
    assert "i32.const 42" in result.wat


def test_undeclared_identifier_is_semantic_error() -> None:
    with pytest.raises(MiniLangError, match="no fue declarada"):
        compile_source("let resultado = desconocida + 1;")


def test_duplicate_variable_is_semantic_error() -> None:
    with pytest.raises(MiniLangError, match="ya fue declarada"):
        compile_source("let x = 1; let x = 2;")


def test_missing_semicolon_is_syntax_error() -> None:
    with pytest.raises(MiniLangError, match="Se esperaba ';'"):
        compile_source("let x = 1")


def test_unknown_character_is_lexical_error() -> None:
    with pytest.raises(MiniLangError, match="Caracter inesperado"):
        compile_source("let x = @42;")

