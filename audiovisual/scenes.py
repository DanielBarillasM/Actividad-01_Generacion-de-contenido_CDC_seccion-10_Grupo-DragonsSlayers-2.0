"""Paquete audiovisual Manim para «De MiniLang a WebAssembly».

Cada escena está diseñada como una unidad de edición con entrada, desarrollo,
respiración para narración y salida. La identidad visual Compiler Signal usa
color semántico constante: fuente, tokens, sintaxis, semántica y destino.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Brace,
    Circle,
    Circumscribe,
    Create,
    CubicBezier,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    FocusOn,
    GrowArrow,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    MovingCameraScene,
    Rectangle,
    ReplacementTransform,
    Restore,
    RoundedRectangle,
    Scene,
    Square,
    SurroundingRectangle,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    Wiggle,
    Write,
    config,
)
from manim.utils.rate_functions import ease_in_out_cubic


INK = "#07131E"
SURFACE = "#0D2130"
PAPER = "#EDF6F9"
MUTED = "#91A9B8"
GRID = "#365364"
SOURCE = "#4DB7FF"
TOKEN = "#FFD166"
SYNTAX = "#B69CFF"
SEMANTIC = "#FF758F"
TARGET = "#57D68D"
DISPLAY_FONT = "Bahnschrift"
CODE_FONT = "Cascadia Code"

config.background_color = INK


def label(text: str, color: str = MUTED, size: int = 24, weight: str = "NORMAL") -> Text:
    return Text(text, font=DISPLAY_FONT, font_size=size, color=color, weight=weight)


def code(text: str, color: str = PAPER, size: int = 30) -> Text:
    return Text(text, font=CODE_FONT, font_size=size, color=color)


def panel(width: float, height: float, color: str = MUTED, opacity: float = 0.94) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.11,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=1.8,
        fill_color=SURFACE,
        fill_opacity=opacity,
    )


def node(text: str, color: str = SYNTAX, width: float = 2.4, height: float = 0.72) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.2,
        fill_color=INK,
        fill_opacity=1,
    )
    value = code(text, color=PAPER, size=21).move_to(box)
    return VGroup(box, value)


def status_pill(text: str, color: str) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.18,
        width=2.05,
        height=0.5,
        stroke_color=color,
        stroke_width=1.5,
        fill_color=color,
        fill_opacity=0.12,
    )
    return VGroup(box, label(text, color=color, size=16, weight="SEMIBOLD").move_to(box))


def technical_grid() -> VGroup:
    lines = VGroup()
    for x in range(-7, 8):
        lines.add(Line(x * RIGHT + 3.9 * DOWN, x * RIGHT + 3.9 * UP))
    for y in range(-4, 5):
        lines.add(Line(7.2 * LEFT + y * UP, 7.2 * RIGHT + y * UP))
    lines.set_stroke(GRID, width=0.55, opacity=0.13)
    return lines


PHASES = [SOURCE, TOKEN, SYNTAX, SEMANTIC, TARGET]


class CompilerVisualMixin:
    section = "De MiniLang a WebAssembly"

    def add_frame(self, accent: str = SOURCE, phase: int = 0) -> None:
        self.add(technical_grid())
        border = Rectangle(
            width=config.frame_width - 0.42,
            height=config.frame_height - 0.42,
            stroke_color=MUTED,
            stroke_width=0.8,
            stroke_opacity=0.28,
        )
        corner_marks = VGroup(
            Line(6.72 * LEFT + 3.55 * UP, 5.95 * LEFT + 3.55 * UP),
            Line(6.72 * LEFT + 3.55 * UP, 6.72 * LEFT + 3.12 * UP),
            Line(6.72 * RIGHT + 3.55 * DOWN, 5.95 * RIGHT + 3.55 * DOWN),
            Line(6.72 * RIGHT + 3.55 * DOWN, 6.72 * RIGHT + 3.12 * DOWN),
        ).set_stroke(accent, width=3.2, opacity=0.9)
        footer = label(self.section, size=15).to_corner(DOWN + RIGHT, buff=0.32)
        rail = VGroup(
            *[
                RoundedRectangle(
                    corner_radius=0.02,
                    width=0.42 if index != phase else 0.82,
                    height=0.055,
                    stroke_width=0,
                    fill_color=color,
                    fill_opacity=1 if index == phase else 0.28,
                )
                for index, color in enumerate(PHASES)
            ]
        ).arrange(RIGHT, buff=0.09).to_corner(DOWN + LEFT, buff=0.34)
        overlay = VGroup(border, corner_marks, footer, rail)
        self.add(overlay)

    def heading(self, kicker: str, title: str, accent: str = SOURCE) -> VGroup:
        kicker_text = label(kicker.upper(), color=accent, size=18, weight="SEMIBOLD")
        title_text = Text(title, font=DISPLAY_FONT, font_size=46, weight="SEMIBOLD", color=PAPER)
        group = VGroup(kicker_text, title_text).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        group.to_edge(UP, buff=0.48).to_edge(LEFT, buff=0.7)
        return group

    def reveal_heading(self, kicker: str, title: str, accent: str) -> VGroup:
        heading = self.heading(kicker, title, accent)
        accent_line = Line(heading.get_left(), heading.get_left() + 1.35 * RIGHT, color=accent, stroke_width=4)
        accent_line.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.13)
        self.play(FadeIn(heading[0], shift=RIGHT * 0.15), Write(heading[1]), Create(accent_line), run_time=1.8)
        return VGroup(heading, accent_line)

    def narration_hold(self, seconds: float = 2.0) -> None:
        self.wait(seconds)


class CompilerScene(CompilerVisualMixin, Scene):
    pass


class CompilerCameraScene(CompilerVisualMixin, MovingCameraScene):
    pass


class HookScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(SOURCE, 0)
        eyebrow = label("UNA LÍNEA · CINCO REPRESENTACIONES", color=SOURCE, size=19, weight="SEMIBOLD")
        title = Text("De MiniLang a WebAssembly", font=DISPLAY_FONT, font_size=61, weight="SEMIBOLD", color=PAPER)
        subtitle = label("¿Qué debe ocurrir antes de que aparezca 42?", size=27)
        header = VGroup(eyebrow, title, subtitle).arrange(DOWN, buff=0.17)
        header.to_edge(UP, buff=0.52)
        self.play(FadeIn(eyebrow, shift=DOWN * 0.12), Write(title), run_time=2.0)
        self.play(FadeIn(subtitle, shift=UP * 0.12), run_time=1.0)

        source_panel = panel(5.75, 2.05, SOURCE).shift(LEFT * 3.55 + DOWN * 0.78)
        line_number = code("01", color=MUTED, size=19).move_to(source_panel.get_left() + RIGHT * 0.42)
        source_code = VGroup(
            code("let resultado = 6 * 7;", size=29),
            code("print(resultado);", color=TARGET, size=29),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(source_panel).shift(RIGHT * 0.28)
        self.play(Create(source_panel), FadeIn(line_number), run_time=1.0)
        self.play(LaggedStart(*[Write(line) for line in source_code], lag_ratio=0.4), run_time=2.0)

        result_ring = Circle(radius=1.05, color=TARGET, stroke_width=2.5).shift(RIGHT * 4.65 + DOWN * 0.76)
        result = Text("42", font=DISPLAY_FONT, font_size=104, weight="SEMIBOLD", color=TARGET).move_to(result_ring)
        route = CubicBezier(
            source_panel.get_right() + 0.1 * RIGHT,
            ORIGIN + 0.8 * UP,
            ORIGIN + 0.8 * DOWN,
            result_ring.get_left() + 0.08 * LEFT,
        ).set_stroke(TARGET, width=3.5, opacity=0.72)
        signal = Dot(route.get_start(), radius=0.105, color=SOURCE)
        self.play(Create(route), FadeIn(signal), GrowFromCenter(result_ring), run_time=1.4)
        self.add_sound("assets/audio/signal.wav", gain=-9)
        self.play(MoveAlongPath(signal, route, rate_func=ease_in_out_cubic), run_time=2.3)
        self.add_sound("assets/audio/success.wav", gain=-7)
        self.play(GrowFromCenter(result), FadeOut(signal), run_time=1.0)
        self.play(
            Circumscribe(source_code[0], color=SOURCE, fade_out=True),
            Circumscribe(result, color=TARGET, fade_out=True),
            run_time=1.8,
        )
        statement = label("El resultado es visible. El proceso todavía no.", color=PAPER, size=22)
        statement.to_edge(DOWN, buff=0.72)
        self.play(FadeIn(statement, shift=UP * 0.12), run_time=1.0)
        self.narration_hold(3.0)


class PipelineScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(TARGET, 4)
        self.reveal_heading("Mapa del compilador", "Una cadena de contratos", TARGET)

        names = ["Código", "Lexer", "Parser", "Semántica", "WAT", "Runtime"]
        subtitles = ["caracteres", "tokens", "AST", "símbolos", "instrucciones", "resultado"]
        colors = [SOURCE, TOKEN, SYNTAX, SEMANTIC, TARGET, TARGET]
        descriptions = [
            "Entrada legible por humanos",
            "Clasifica fragmentos con posición",
            "Construye una jerarquía",
            "Comprueba nombres y tipos",
            "Emite operaciones de pila",
            "Valida, instancia y ejecuta",
        ]
        boxes = VGroup()
        for index, (name, subtitle, color) in enumerate(zip(names, subtitles, colors), start=1):
            box = RoundedRectangle(
                corner_radius=0.08,
                width=1.86,
                height=1.45,
                stroke_color=color,
                stroke_width=2,
                fill_color=SURFACE,
                fill_opacity=1,
            )
            number = label(f"0{index}", color=color, size=15, weight="SEMIBOLD").move_to(box.get_corner(UP + LEFT) + 0.2 * (RIGHT + DOWN))
            copy = VGroup(code(name, size=20), label(subtitle, size=15)).arrange(DOWN, buff=0.13).move_to(box)
            boxes.add(VGroup(box, number, copy))
        boxes.arrange(RIGHT, buff=0.27).shift(DOWN * 0.15)

        arrows = VGroup(
            *[
                Arrow(boxes[index].get_right(), boxes[index + 1].get_left(), color=MUTED, stroke_width=2.2, buff=0.07)
                for index in range(len(boxes) - 1)
            ]
        )
        for index, box in enumerate(boxes):
            self.play(GrowFromCenter(box), run_time=0.75)
            if index < len(arrows):
                self.play(GrowArrow(arrows[index]), run_time=0.45)

        detail_box = panel(8.0, 0.82, MUTED).to_edge(DOWN, buff=0.75)
        detail = label(descriptions[0], color=PAPER, size=21).move_to(detail_box)
        self.play(Create(detail_box), FadeIn(detail), run_time=0.9)

        signal = Dot(boxes[0].get_center(), radius=0.115, color=SOURCE)
        halo = Circle(radius=0.76, color=SOURCE, stroke_width=2).move_to(boxes[0])
        self.play(FadeIn(signal), Create(halo), run_time=0.7)
        for index in range(1, len(boxes)):
            next_detail = label(descriptions[index], color=PAPER, size=21).move_to(detail_box)
            self.add_sound("assets/audio/click.wav", gain=-14)
            self.play(
                signal.animate.move_to(boxes[index]).set_color(colors[index]),
                halo.animate.move_to(boxes[index]).set_color(colors[index]),
                ReplacementTransform(detail, next_detail),
                run_time=1.35,
                rate_func=ease_in_out_cubic,
            )
            detail = next_detail
            self.play(Indicate(boxes[index], color=colors[index], scale_factor=1.04), run_time=0.75)
        self.play(FadeOut(signal), FadeOut(halo), run_time=0.7)
        self.narration_hold(3.2)


class LexerScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(TOKEN, 1)
        self.reveal_heading("Análisis léxico", "Un escáner con memoria de posición", TOKEN)

        source_panel = panel(12.1, 1.25, SOURCE).shift(UP * 0.75)
        parts = [
            ("let", SOURCE),
            ("resultado", PAPER),
            ("=", PAPER),
            ("6", TOKEN),
            ("*", PAPER),
            ("7", TOKEN),
            (";", PAPER),
        ]
        source_parts = VGroup(*[code(text, color=color, size=32) for text, color in parts]).arrange(RIGHT, buff=0.32).move_to(source_panel)
        coordinates = label("línea 1 · columnas 1—22", color=MUTED, size=17).next_to(source_panel, DOWN, buff=0.12).align_to(source_panel, LEFT)
        self.play(Create(source_panel), LaggedStart(*[Write(part) for part in source_parts], lag_ratio=0.16), run_time=2.2)
        self.play(FadeIn(coordinates), run_time=0.7)

        token_names = ["LET", "IDENTIFIER", "EQUAL", "NUMBER", "STAR", "NUMBER", "SEMICOLON"]
        token_cards = VGroup()
        for token_name in token_names:
            width = 1.82 if token_name in {"IDENTIFIER", "SEMICOLON"} else 1.38
            card = RoundedRectangle(
                corner_radius=0.06,
                width=width,
                height=0.72,
                stroke_color=TOKEN,
                stroke_width=1.5,
                fill_color=SURFACE,
                fill_opacity=1,
            )
            token_cards.add(VGroup(card, code(token_name, color=TOKEN, size=15).move_to(card)))
        token_cards.arrange(RIGHT, buff=0.12).shift(DOWN * 1.08)

        scanner = SurroundingRectangle(source_parts[0], color=TOKEN, buff=0.13, stroke_width=2.5)
        scanner_label = status_pill("SCANNER ACTIVO", TOKEN).scale(0.82).next_to(source_panel, UP, buff=0.14).align_to(source_panel, RIGHT)
        self.play(Create(scanner), FadeIn(scanner_label), run_time=0.8)
        for index, (source_part, token_card) in enumerate(zip(source_parts, token_cards)):
            if index:
                next_scanner = SurroundingRectangle(source_part, color=TOKEN, buff=0.13, stroke_width=2.5)
                self.play(Transform(scanner, next_scanner), run_time=0.55)
            self.add_sound("assets/audio/click.wav", gain=-14)
            self.play(TransformFromCopy(source_part, token_card), run_time=0.8)
            self.wait(0.25)

        note = VGroup(
            label("Lexema", color=SOURCE, size=18, weight="SEMIBOLD"),
            label("fragmento original", size=18),
            label("Token", color=TOKEN, size=18, weight="SEMIBOLD"),
            label("categoría reconocida", size=18),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.72)
        divider = Line(note[1].get_right() + 0.2 * RIGHT, note[2].get_left() + 0.2 * LEFT, color=MUTED, stroke_width=1)
        self.play(FadeOut(scanner), FadeOut(scanner_label), FadeIn(note), Create(divider), run_time=1.1)
        self.play(LaggedStart(*[Indicate(card, color=TOKEN, scale_factor=1.04) for card in token_cards], lag_ratio=0.12), run_time=2.0)
        self.narration_hold(3.0)


class GrammarScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(SYNTAX, 2)
        self.reveal_heading("Gramática", "Las reglas deciden la precedencia", SYNTAX)

        grammar_box = panel(5.55, 3.85, SYNTAX).shift(LEFT * 3.55 + DOWN * 0.45)
        grammar_title = label("GRAMÁTICA REDUCIDA", color=SYNTAX, size=17, weight="SEMIBOLD")
        grammar_lines = VGroup(
            code("expr   → term ((+|-) term)*", size=20),
            code("term   → factor ((*|/) factor)*", size=20),
            code("factor → NUMBER", size=20),
            code("       | IDENTIFIER", size=20),
            code("       | '(' expr ')'", size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        grammar_content = VGroup(grammar_title, grammar_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(grammar_box)
        self.play(Create(grammar_box), FadeIn(grammar_title), run_time=1.0)
        self.play(LaggedStart(*[Write(line) for line in grammar_lines], lag_ratio=0.2), run_time=2.6)

        expression = VGroup(
            code("6", color=TOKEN, size=47),
            code("+", color=SYNTAX, size=47),
            code("7", color=TOKEN, size=47),
            code("*", color=SYNTAX, size=47),
            code("2", color=TOKEN, size=47),
        ).arrange(RIGHT, buff=0.28).shift(RIGHT * 3.55 + UP * 0.65)
        self.play(LaggedStart(*[Write(part) for part in expression], lag_ratio=0.14), run_time=1.6)

        multiply_group = VGroup(expression[2], expression[3], expression[4])
        multiply_box = SurroundingRectangle(multiply_group, color=TOKEN, buff=0.19, stroke_width=2.5)
        multiply_label = status_pill("TERM PRIMERO", TOKEN).scale(0.86).next_to(multiply_box, DOWN, buff=0.22)
        self.play(Create(multiply_box), FadeIn(multiply_label, shift=UP * 0.1), run_time=1.0)
        self.play(Indicate(grammar_lines[1], color=TOKEN, scale_factor=1.04), run_time=1.2)

        whole_box = SurroundingRectangle(expression, color=SYNTAX, buff=0.36, stroke_width=2.5)
        expr_label = status_pill("EXPR DESPUÉS", SYNTAX).scale(0.86).next_to(whole_box, DOWN, buff=0.75)
        self.play(Transform(multiply_box, whole_box), ReplacementTransform(multiply_label, expr_label), run_time=1.25)
        self.play(Indicate(grammar_lines[0], color=SYNTAX, scale_factor=1.04), run_time=1.2)

        result = VGroup(
            label("Agrupación resultante", size=18),
            code("6 + (7 * 2)", color=PAPER, size=30),
        ).arrange(DOWN, buff=0.18).shift(RIGHT * 3.55 + DOWN * 1.65)
        self.play(FadeIn(result[0]), TransformFromCopy(expression, result[1]), run_time=1.3)
        self.play(Circumscribe(result[1], color=SYNTAX, fade_out=True), run_time=1.5)
        self.narration_hold(3.0)


class AstScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(SYNTAX, 2)
        self.reveal_heading("Análisis sintáctico", "El texto se convierte en jerarquía", SYNTAX)

        root = node("Add", width=1.55).shift(UP * 0.55)
        six = node("6", color=TOKEN, width=1.15).shift(LEFT * 3.05 + DOWN * 0.85)
        multiply = node("Multiply", width=2.05).shift(RIGHT * 2.05 + DOWN * 0.85)
        seven = node("7", color=TOKEN, width=1.15).shift(RIGHT * 0.9 + DOWN * 2.38)
        two = node("2", color=TOKEN, width=1.15).shift(RIGHT * 3.25 + DOWN * 2.38)
        edges = VGroup(
            Line(root.get_bottom(), six.get_top(), color=SYNTAX, stroke_width=2),
            Line(root.get_bottom(), multiply.get_top(), color=SYNTAX, stroke_width=2),
            Line(multiply.get_bottom(), seven.get_top(), color=SYNTAX, stroke_width=2),
            Line(multiply.get_bottom(), two.get_top(), color=SYNTAX, stroke_width=2),
        )
        source = code("6 + 7 * 2", color=MUTED, size=24).shift(LEFT * 4.55 + UP * 1.35)
        source_box = SurroundingRectangle(source, color=SOURCE, buff=0.15, stroke_width=1.5)
        self.play(Create(source_box), Write(source), run_time=1.2)
        self.play(GrowFromCenter(root), run_time=0.9)
        self.play(Create(edges[:2]), AnimationGroup(GrowFromCenter(six), GrowFromCenter(multiply)), run_time=1.6)
        self.play(Create(edges[2:]), AnimationGroup(GrowFromCenter(seven), GrowFromCenter(two)), run_time=1.6)

        focus_group = VGroup(multiply, seven, two, edges[2], edges[3])
        context_group = VGroup(root, six, edges[0], edges[1])
        focus_group.save_state()
        context_group.save_state()
        self.play(
            focus_group.animate.scale(1.1),
            context_group.animate.set_opacity(0.22),
            FadeOut(source),
            FadeOut(source_box),
            run_time=1.5,
            rate_func=ease_in_out_cubic,
        )
        self.play(FocusOn(multiply), Circumscribe(multiply, color=TOKEN, fade_out=True), run_time=1.5)
        precedence = label("La multiplicación vive más abajo: se evalúa primero.", color=TOKEN, size=19)
        precedence.next_to(multiply, UP, buff=0.32)
        self.play(FadeIn(precedence, shift=DOWN * 0.08), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(precedence), Restore(focus_group), Restore(context_group), run_time=1.5)

        value_14 = status_pill("valor = 14", TOKEN).scale(0.82).next_to(multiply, RIGHT, buff=0.28)
        value_20 = status_pill("valor = 20", TARGET).scale(0.82).next_to(root, RIGHT, buff=0.3)
        self.play(TransformFromCopy(VGroup(seven, two), value_14), run_time=1.2)
        self.play(Indicate(multiply, color=TOKEN), run_time=0.9)
        self.play(TransformFromCopy(VGroup(six, value_14), value_20), run_time=1.2)
        self.play(Indicate(root, color=TARGET), run_time=0.9)
        caption = label("La forma del árbol hace explícito el orden.", size=21).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(caption), run_time=0.8)
        self.narration_hold(3.0)


class SemanticScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(SEMANTIC, 3)
        self.reveal_heading("Análisis semántico", "La estructura necesita contexto", SEMANTIC)

        symbol_box = panel(4.7, 3.7, SEMANTIC).shift(RIGHT * 4.0 + DOWN * 0.42)
        symbol_title = VGroup(
            label("TABLA DE SÍMBOLOS", color=SEMANTIC, size=17, weight="SEMIBOLD"),
            Line(2.0 * LEFT, 2.0 * RIGHT, color=SEMANTIC, stroke_width=1.2),
        ).arrange(DOWN, buff=0.18).move_to(symbol_box).shift(UP * 1.15)
        header = VGroup(code("nombre", color=MUTED, size=16), code("tipo", color=MUTED, size=16), code("local", color=MUTED, size=16)).arrange(RIGHT, buff=0.58)
        header.move_to(symbol_box).shift(UP * 0.55)
        self.play(Create(symbol_box), FadeIn(symbol_title), FadeIn(header), run_time=1.2)

        declaration_box = panel(7.0, 1.25, SOURCE).shift(LEFT * 2.45 + UP * 0.75)
        declaration = code("let resultado = 6 * 7;", size=28).move_to(declaration_box)
        self.play(Create(declaration_box), Write(declaration), run_time=1.4)
        row = VGroup(code("resultado", size=18), code("i32", color=TOKEN, size=18), code("0", color=TARGET, size=18)).arrange(RIGHT, buff=0.78)
        row.move_to(symbol_box).shift(DOWN * 0.18)
        check = label("OK · declaración registrada", color=TARGET, size=18).next_to(declaration_box, DOWN, buff=0.18).align_to(declaration_box, LEFT)
        self.play(TransformFromCopy(declaration, row), FadeIn(check), run_time=1.3)
        self.play(Indicate(row, color=TARGET), run_time=0.9)

        invalid_box = panel(7.0, 1.25, SEMANTIC).shift(LEFT * 2.45 + DOWN * 1.08)
        left = code("print(", size=28)
        unknown = code("desconocida", color=SEMANTIC, size=28)
        right = code(");", size=28)
        invalid = VGroup(left, unknown, right).arrange(RIGHT, buff=0.02).move_to(invalid_box)
        self.play(Create(invalid_box), Write(invalid), run_time=1.35)
        underline = Line(unknown.get_left() + DOWN * 0.3, unknown.get_right() + DOWN * 0.3, color=SEMANTIC, stroke_width=4)
        missing = VGroup(code("desconocida", color=SEMANTIC, size=18), code("—", color=MUTED, size=18), code("ERROR", color=SEMANTIC, size=18)).arrange(RIGHT, buff=0.55)
        missing.move_to(symbol_box).shift(DOWN * 0.8)
        self.add_sound("assets/audio/error.wav", gain=-9)
        self.play(Create(underline), FadeIn(missing, shift=UP * 0.12), run_time=1.0)

        diagnostic = panel(10.8, 0.72, SEMANTIC).to_edge(DOWN, buff=0.72)
        diagnostic_text = VGroup(
            status_pill("E001", SEMANTIC).scale(0.72),
            label("línea 2, columna 7 · variable 'desconocida' no declarada", color=PAPER, size=19),
        ).arrange(RIGHT, buff=0.28).move_to(diagnostic)
        self.play(Create(diagnostic), FadeIn(diagnostic_text), run_time=1.2)
        self.play(Wiggle(unknown, scale_value=1.06, rotation_angle=0.03), run_time=1.1)
        self.narration_hold(3.2)


class OptimizationScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(TOKEN, 3)
        self.reveal_heading("Optimización local", "Mismo significado, menos trabajo", TOKEN)

        before_box = panel(4.75, 3.15, SYNTAX).shift(LEFT * 3.75 + DOWN * 0.35)
        before_title = label("ANTES · 3 INSTRUCCIONES", color=SYNTAX, size=17, weight="SEMIBOLD").next_to(before_box, UP, buff=0.18)
        before = VGroup(
            code("i32.const 6", size=25),
            code("i32.const 7", size=25),
            code("i32.mul", color=SYNTAX, size=25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(before_box)
        self.play(Create(before_box), FadeIn(before_title), run_time=1.0)
        self.play(LaggedStart(*[Write(row) for row in before], lag_ratio=0.3), run_time=2.0)

        fold = VGroup(
            Circle(radius=0.72, color=TOKEN, stroke_width=2.4, fill_color=TOKEN, fill_opacity=0.08),
            label("FOLD", color=TOKEN, size=17, weight="SEMIBOLD"),
        ).shift(DOWN * 0.35)
        arrow_left = Arrow(before_box.get_right(), fold.get_left(), color=TOKEN, buff=0.14, stroke_width=3)
        self.add_sound("assets/audio/signal.wav", gain=-11)
        self.play(GrowArrow(arrow_left), GrowFromCenter(fold), run_time=1.3)
        self.play(Indicate(before[0], color=TOKEN), Indicate(before[1], color=TOKEN), run_time=1.0)
        equation = code("6 × 7 = 42", color=TOKEN, size=25).next_to(fold, DOWN, buff=0.32)
        self.play(TransformFromCopy(VGroup(before[0], before[1]), equation), run_time=1.1)

        after_box = panel(4.75, 3.15, TARGET).shift(RIGHT * 3.75 + DOWN * 0.35)
        after_title = label("DESPUÉS · 1 INSTRUCCIÓN", color=TARGET, size=17, weight="SEMIBOLD").next_to(after_box, UP, buff=0.18)
        after = code("i32.const 42", color=TARGET, size=28).move_to(after_box)
        arrow_right = Arrow(fold.get_right(), after_box.get_left(), color=TOKEN, buff=0.14, stroke_width=3)
        self.play(GrowArrow(arrow_right), Create(after_box), FadeIn(after_title), run_time=1.2)
        self.play(TransformFromCopy(equation, after), run_time=1.2)

        saved = status_pill("−2 operaciones en runtime", TARGET).scale(0.95).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(saved, shift=UP * 0.12), run_time=0.8)
        self.play(Circumscribe(after, color=TARGET, fade_out=True), run_time=1.5)
        self.narration_hold(3.0)


class StackScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(TARGET, 4)
        self.reveal_heading("Generación de código", "WebAssembly trabaja con una pila", TARGET)

        instructions = [
            ("i32.const 6", "empuja 6"),
            ("i32.const 7", "empuja 7"),
            ("i32.mul", "consume dos valores"),
            ("local.set $resultado", "guarda 42"),
            ("local.get $resultado", "recupera 42"),
            ("call $print_i32", "llama al host"),
        ]
        rows = VGroup()
        for opcode, description in instructions:
            row_box = RoundedRectangle(corner_radius=0.04, width=5.45, height=0.58, stroke_color=GRID, stroke_width=1, fill_color=SURFACE, fill_opacity=0.92)
            opcode_text = code(opcode, size=20).move_to(row_box).align_to(row_box, LEFT).shift(RIGHT * 0.22)
            description_text = label(description, size=14).move_to(row_box).align_to(row_box, RIGHT).shift(LEFT * 0.22)
            rows.add(VGroup(row_box, opcode_text, description_text))
        rows.arrange(DOWN, buff=0.08).shift(LEFT * 3.65 + DOWN * 0.38)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.12) for row in rows], lag_ratio=0.13), run_time=2.2)

        pointer = Arrow(LEFT * 6.75, LEFT * 6.05, color=TARGET, buff=0, stroke_width=4).move_to(rows[0].get_left() + LEFT * 0.42)
        stack_frame = VGroup(
            Rectangle(width=2.55, height=3.4, stroke_color=TARGET, stroke_width=2.2),
            label("PILA", color=TARGET, size=18, weight="SEMIBOLD").shift(UP * 1.95),
        ).shift(RIGHT * 2.55 + DOWN * 0.42)
        local_box = panel(2.75, 1.35, SOURCE).shift(RIGHT * 5.4 + DOWN * 0.55)
        local_title = label("LOCAL 0", color=SOURCE, size=15, weight="SEMIBOLD").next_to(local_box, UP, buff=0.1)
        local_value = code("—", color=MUTED, size=30).move_to(local_box)
        self.play(FadeIn(pointer), Create(stack_frame[0]), FadeIn(stack_frame[1]), Create(local_box), FadeIn(local_title), FadeIn(local_value), run_time=1.4)

        def stack_block(value: str, color: str, y: float) -> VGroup:
            box = RoundedRectangle(corner_radius=0.05, width=2.12, height=0.72, stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=0.12)
            return VGroup(box, code(value, color=color, size=27).move_to(box)).move_to(stack_frame[0].get_bottom() + y * UP)

        six = stack_block("6", TOKEN, 0.48)
        seven = stack_block("7", TOKEN, 1.28)
        forty_two = stack_block("42", TARGET, 0.48)

        self.add_sound("assets/audio/click.wav", gain=-13)
        self.play(Indicate(rows[0], color=TARGET), FadeIn(six, shift=UP * 0.25), run_time=1.25)
        self.wait(0.6)
        self.play(pointer.animate.move_to(rows[1].get_left() + LEFT * 0.42), run_time=0.65)
        self.add_sound("assets/audio/click.wav", gain=-13)
        self.play(Indicate(rows[1], color=TARGET), FadeIn(seven, shift=UP * 0.25), run_time=1.25)
        self.wait(0.6)
        self.play(pointer.animate.move_to(rows[2].get_left() + LEFT * 0.42), run_time=0.65)
        operation = label("7 × 6", color=TOKEN, size=19).next_to(stack_frame, UP, buff=0.16)
        self.play(FadeIn(operation), Indicate(rows[2], color=TARGET), run_time=0.8)
        self.add_sound("assets/audio/signal.wav", gain=-10)
        self.play(ReplacementTransform(VGroup(six, seven), forty_two), run_time=1.4)
        self.play(ReplacementTransform(operation, label("= 42", color=TARGET, size=19).move_to(operation)), run_time=0.7)
        self.wait(0.7)

        self.play(pointer.animate.move_to(rows[3].get_left() + LEFT * 0.42), run_time=0.65)
        stored = code("42", color=TARGET, size=30).move_to(local_box)
        self.play(Indicate(rows[3], color=TARGET), TransformFromCopy(forty_two, stored), FadeOut(local_value), run_time=1.2)
        self.play(FadeOut(forty_two), run_time=0.65)
        self.wait(0.7)
        self.play(pointer.animate.move_to(rows[4].get_left() + LEFT * 0.42), run_time=0.65)
        recalled = stack_block("42", TARGET, 0.48)
        self.play(Indicate(rows[4], color=TARGET), TransformFromCopy(stored, recalled), run_time=1.2)
        self.wait(0.7)
        self.play(pointer.animate.move_to(rows[5].get_left() + LEFT * 0.42), run_time=0.65)
        outgoing = Dot(recalled.get_center(), radius=0.1, color=TARGET)
        route = Arrow(stack_frame.get_right(), local_box.get_right() + 1.0 * RIGHT, color=TARGET, stroke_width=3.5, buff=0.08)
        self.add_sound("assets/audio/success.wav", gain=-8)
        self.play(Indicate(rows[5], color=TARGET), GrowArrow(route), FadeIn(outgoing), run_time=1.1)
        self.play(outgoing.animate.move_to(route.get_end()), FadeOut(recalled), run_time=1.25)
        callout = status_pill("SALIDA → 42", TARGET).scale(0.9).next_to(local_box, DOWN, buff=0.23)
        self.play(FadeIn(callout, shift=UP * 0.1), FadeOut(outgoing), run_time=0.9)
        self.narration_hold(3.2)


class RuntimeScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(TARGET, 4)
        self.reveal_heading("Runtime", "El módulo cruza la frontera con el host", TARGET)

        steps = VGroup(
            status_pill("1 · VALIDAR", SOURCE),
            status_pill("2 · INSTANCIAR", TOKEN),
            status_pill("3 · EJECUTAR", TARGET),
        ).arrange(RIGHT, buff=0.28).shift(UP * 1.68)
        self.play(LaggedStart(*[FadeIn(step, shift=UP * 0.12) for step in steps], lag_ratio=0.28), run_time=1.8)

        wasm_box = panel(5.0, 3.25, TARGET).shift(LEFT * 3.55 + DOWN * 0.65)
        wasm_title = label("MÓDULO WASM", color=TARGET, size=18, weight="SEMIBOLD").move_to(wasm_box.get_top() + DOWN * 0.26)
        wasm_code = VGroup(
            code("local.get $resultado", size=20),
            code("call $print_i32", color=TARGET, size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(wasm_box)
        host_box = panel(5.0, 3.25, SOURCE).shift(RIGHT * 3.55 + DOWN * 0.65)
        host_title = label("ENTORNO HOST", color=SOURCE, size=18, weight="SEMIBOLD").move_to(host_box.get_top() + DOWN * 0.26)
        host_code = VGroup(
            code("env.print_i32(value)", color=SOURCE, size=20),
            label("función importada", size=17),
        ).arrange(DOWN, buff=0.27).move_to(host_box).shift(UP * 0.5)
        terminal = RoundedRectangle(corner_radius=0.06, width=3.9, height=1.0, stroke_color=MUTED, stroke_width=1.4, fill_color=INK, fill_opacity=1)
        terminal.move_to(host_box).shift(DOWN * 0.95)
        prompt = code(">", color=MUTED, size=24).move_to(terminal).align_to(terminal, LEFT).shift(RIGHT * 0.25)
        self.play(Create(wasm_box), FadeIn(wasm_title), Write(wasm_code), run_time=1.8)
        self.play(Indicate(steps[0], color=SOURCE), run_time=1.0)
        self.play(Create(host_box), FadeIn(host_title), FadeIn(host_code), Create(terminal), FadeIn(prompt), run_time=1.7)
        self.play(Indicate(steps[1], color=TOKEN), run_time=1.0)

        bridge = Arrow(wasm_box.get_right(), host_box.get_left(), color=TARGET, stroke_width=4, buff=0.12)
        bridge_label = label("import env.print_i32", color=TARGET, size=17).next_to(bridge, UP, buff=0.15)
        packet = Dot(bridge.get_start(), radius=0.11, color=TARGET)
        self.play(GrowArrow(bridge), FadeIn(bridge_label), FadeIn(packet), run_time=1.2)
        self.play(Indicate(steps[2], color=TARGET), run_time=1.0)
        self.add_sound("assets/audio/signal.wav", gain=-10)
        self.play(packet.animate.move_to(bridge.get_end()), run_time=1.7, rate_func=ease_in_out_cubic)
        self.play(Indicate(host_code[0], color=SOURCE), run_time=0.9)
        output = code("42", color=TARGET, size=34).next_to(prompt, RIGHT, buff=0.22)
        self.add_sound("assets/audio/success.wav", gain=-7)
        self.play(Write(output), FadeOut(packet), run_time=1.0)
        self.play(Circumscribe(VGroup(prompt, output), color=TARGET, fade_out=True), run_time=1.6)
        takeaway = label("El compilador tradujo; el runtime hizo observable el resultado.", color=PAPER, size=20)
        takeaway.to_edge(DOWN, buff=0.7)
        self.play(FadeIn(takeaway, shift=UP * 0.1), run_time=0.9)
        self.narration_hold(3.2)


class CreditsScene(CompilerScene):
    def construct(self) -> None:
        self.add_frame(TARGET, 4)
        course = label("Universidad del Valle de Guatemala", color=TARGET, size=24, weight="SEMIBOLD").shift(UP * 2.75)
        title = Text("DragonsSlayers 2.0", font=DISPLAY_FONT, font_size=57, weight="SEMIBOLD", color=PAPER).shift(UP * 1.72)
        members = VGroup(
            label("Pablo Daniel Barillas Moreno", color=PAPER, size=27),
            label("Hugo Daniel Barillas Ajín", color=PAPER, size=27),
            label("Ernesto Ascencio", color=PAPER, size=27),
        ).arrange(DOWN, buff=0.3).shift(DOWN * 0.05)
        footer = VGroup(
            label("Construcción de Compiladores · Sección 10", size=21),
            label("Contenido original · Creative Commons Attribution 4.0", size=17),
        ).arrange(DOWN, buff=0.2).shift(DOWN * 2.55)
        phase_bar = VGroup(
            *[
                RoundedRectangle(corner_radius=0.02, width=1.25, height=0.08, stroke_width=0, fill_color=color, fill_opacity=1)
                for color in PHASES
            ]
        ).arrange(RIGHT, buff=0.08).shift(DOWN * 1.55)

        self.play(FadeIn(course, shift=DOWN * 0.12), Write(title), run_time=1.8)
        self.play(LaggedStart(*[FadeIn(member, shift=UP * 0.14) for member in members], lag_ratio=0.32), run_time=2.1)
        self.play(LaggedStart(*[GrowFromCenter(segment) for segment in phase_bar], lag_ratio=0.18), run_time=1.5)
        self.play(FadeIn(footer), run_time=1.0)
        self.play(Circumscribe(title, color=TARGET, fade_out=True), run_time=1.8)
        self.narration_hold(4.2)
