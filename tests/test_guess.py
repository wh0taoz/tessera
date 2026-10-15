from tessera.guess import Enumerator, guess
from tessera.parser import parse
from tessera.syntax import pretty
from tessera.typecheck import holes_of
from tessera.types import BOOL, INT, TArrow


def guesses(src: str, **kwargs: int) -> list[str]:
    [hole] = holes_of(parse(src))
    return [pretty(c.expr) for c in guess(hole, **kwargs)]


def test_prefers_variables_over_literals() -> None:
    result = guesses("let n : int = 5 in n + ?", top=3)
    assert result[0] == "n"
    assert "0" in result or "1" in result


def test_prefers_most_recent_variable() -> None:
    result = guesses("let a : int = 1 in let b : int = 2 in ?h * 2")
    assert result[:2] == ["b", "a"]


def test_function_hole_uses_parameter() -> None:
    result = guesses("let k : int = 3 in let ok : bool = ?f 4 in ok", top=10)
    assert all(r.startswith("fun (x: int) ->") for r in result)
    # The best guess should relate the argument to the context, not ignore it.
    body = result[0].split("->", 1)[1].split()
    assert "x" in body and "k" in body


def test_applies_functions_in_scope() -> None:
    src = "let inc : int -> int = fun (x: int) -> x + 1 in let r : int = ? in r"
    assert "inc 0" in guesses(src, top=20, max_size=2)


def test_every_candidate_is_well_typed() -> None:
    env = (("n", INT), ("p", BOOL), ("f", TArrow(INT, BOOL)))
    for n in range(1, 5):
        for term in Enumerator().terms(env, BOOL, n):
            src = f"let n : int = 1 in let p : bool = true in " \
                  f"let f : int -> bool = fun (x: int) -> x < 2 in " \
                  f"let r : bool = {pretty(term)} in r"
            assert holes_of(parse(src)) == []


def test_unknown_goal_gives_no_guesses() -> None:
    assert guesses("?") == []
