import pytest

from tessera.parser import parse
from tessera.typecheck import TypeError_, holes_of
from tessera.types import BOOL, INT, TArrow


def only_hole(src: str):  # type: ignore[no-untyped-def]
    holes = holes_of(parse(src))
    assert len(holes) == 1
    return holes[0]


def test_hole_as_function_argument() -> None:
    hole = only_hole("let f : int -> bool = fun (x: int) -> x < 3 in f ?h")
    assert hole.expected == INT
    assert hole.visible() == {"f": TArrow(INT, BOOL)}


def test_hole_in_let_value() -> None:
    assert only_hole("let x : bool = ? in x").expected == BOOL


def test_hole_as_function_gets_arrow_type() -> None:
    assert only_hole("let b : bool = ?f 3 in b").expected == TArrow(INT, BOOL)


def test_hole_in_lambda_sees_parameter() -> None:
    hole = only_hole("let f : int -> int = fun (n: int) -> ? in f 1")
    assert hole.expected == INT
    assert "n" in hole.visible()


def test_hole_in_synth_position_has_unknown_type() -> None:
    assert only_hole("?").expected is None


def test_type_errors() -> None:
    with pytest.raises(TypeError_):
        holes_of(parse("1 + true"))
    with pytest.raises(TypeError_):
        holes_of(parse("y"))
