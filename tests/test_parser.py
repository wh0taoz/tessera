import pytest

from tessera.parser import ParseError, parse
from tessera.syntax import App, BinOp, Hole, IntLit, Lam, Let, Var, pretty
from tessera.types import INT, TArrow


def test_named_and_anonymous_holes() -> None:
    assert parse("?goal") == Hole("goal")
    assert parse("?") == Hole("1")


def test_application_is_left_associative() -> None:
    assert parse("f a b") == App(App(Var("f"), Var("a")), Var("b"))


def test_operator_precedence() -> None:
    assert parse("1 + 2 * 3") == BinOp("+", IntLit(1), BinOp("*", IntLit(2), IntLit(3)))


def test_let_and_lambda() -> None:
    e = parse("let f : int -> int = fun (x: int) -> x in f ?")
    assert e == Let(
        "f",
        TArrow(INT, INT),
        Lam("x", INT, Var("x")),
        App(Var("f"), Hole("1")),
    )


def test_keywords_are_not_identifiers_but_prefixes_are() -> None:
    assert parse("letter") == Var("letter")


def test_comments_are_ignored() -> None:
    assert parse("# a comment\n42") == IntLit(42)


def test_pretty_round_trips() -> None:
    src = "let f : int -> int = fun (x: int) -> x + 1 in f (f ?h)"
    assert parse(pretty(parse(src))) == parse(src)


def test_parse_error() -> None:
    with pytest.raises(ParseError):
        parse("let x = in")
