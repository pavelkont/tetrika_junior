import pytest
from solution_1 import strict


@strict
def add(a: int, b: int) -> int:
    return a + b


@strict
def concat(a: str, b: str) -> str:
    return a + b


@strict
def logic(x: bool, y: bool) -> bool:
    return x and y


def test_add_correct_types(capfd):
    assert add(2, 3) == 5


def test_add_type_error(capfd):
    add(2, 3.5)
    out, _ = capfd.readouterr()
    assert "Аргумент 'b' должет быть int, получен float." in out


def test_concat_correct_types(capfd):
    assert concat("a", "b") == "ab"


def test_concat_type_error(capfd):
    concat("a", 1)
    out, _ = capfd.readouterr()
    assert "Аргумент 'b' должет быть str, получен int." in out


def test_logic_correct_types(capfd):
    assert logic(True, False) is False


def test_logic_type_error(capfd):
    logic(True, "False")
    out, _ = capfd.readouterr()
    assert "Аргумент 'y' должет быть bool, получен str." in out
