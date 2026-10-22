from __future__ import annotations

from dataclasses import dataclass

from .ast_nodes import Program
from .codegen import WatGenerator
from .lexer import Lexer
from .optimizer import optimize_program
from .parser import Parser
from .semantic import SemanticAnalyzer, Symbol
from .tokens import Token


@dataclass(frozen=True, slots=True)
class CompilationResult:
    tokens: tuple[Token, ...]
    ast: Program
    optimized_ast: Program
    symbols: tuple[Symbol, ...]
    wat: str


def compile_source(source: str, *, optimize: bool = False) -> CompilationResult:
    tokens = tuple(Lexer(source).scan_tokens())
    ast = Parser(list(tokens)).parse()
    symbols = SemanticAnalyzer().analyze(ast)
    optimized_ast = optimize_program(ast) if optimize else ast
    wat = WatGenerator(symbols).generate(optimized_ast)
    return CompilationResult(tokens, ast, optimized_ast, symbols, wat)


def execute_wat(wat: str) -> list[int]:
    try:
        import wasmtime
    except ImportError as error:
        raise RuntimeError(
            "Wasmtime no esta instalado. Ejecute: python -m pip install wasmtime"
        ) from error

    engine = wasmtime.Engine()
    module = wasmtime.Module(engine, wat)
    store = wasmtime.Store(engine)
    linker = wasmtime.Linker(engine)
    output: list[int] = []

    print_type = wasmtime.FuncType([wasmtime.ValType.i32()], [])
    print_function = wasmtime.Func(store, print_type, lambda value: output.append(value))
    linker.define(store, "env", "print_i32", print_function)

    instance = linker.instantiate(store, module)
    main = instance.exports(store)["main"]
    main(store)
    return output

