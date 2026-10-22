from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ast_nodes import ast_to_dict
from .compiler import compile_source, execute_wat
from .errors import MiniLangError


def main() -> int:
    parser = argparse.ArgumentParser(description="Compilador educativo MiniLang -> WebAssembly")
    parser.add_argument("source", type=Path, help="Archivo .mini")
    parser.add_argument("--optimize", action="store_true", help="Activa constant folding")
    parser.add_argument("--tokens", action="store_true", help="Muestra los tokens")
    parser.add_argument("--ast", action="store_true", help="Muestra el AST como JSON")
    parser.add_argument("--wat", action="store_true", help="Muestra el WebAssembly textual")
    parser.add_argument("--run", action="store_true", help="Ejecuta el modulo con Wasmtime")
    args = parser.parse_args()

    try:
        result = compile_source(args.source.read_text(encoding="utf-8"), optimize=args.optimize)
    except MiniLangError as error:
        print(f"Error: {error}")
        return 1

    if args.tokens:
        print("\n".join(token.label() for token in result.tokens))
    if args.ast:
        print(json.dumps(ast_to_dict(result.optimized_ast), indent=2, ensure_ascii=False))
    if args.wat:
        print(result.wat, end="")
    if args.run:
        for value in execute_wat(result.wat):
            print(value)
    if not any((args.tokens, args.ast, args.wat, args.run)):
        print(result.wat, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

