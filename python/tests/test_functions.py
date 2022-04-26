import pytest
import datetime
from to_test import even_odd, sum_all, time_of_day


@pytest.mark.parametrize("test_input,expected", [(5, "odd"), (3, "odd"), (193, "odd")])
def test_evenodd_odd(test_input, expected):
    assert even_odd(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [(4, "even"), (1000, "even"), (194, "even")])
def test_evenodd_even(test_input, expected):
    assert even_odd(test_input) == expected


def test_evenodd_float():
    assert even_odd(4.5) is None


@pytest.mark.parametrize("test_input", [None, "str"])
def test_evenodd_unexpected(test_input):
    with pytest.raises(TypeError):
        even_odd(test_input)


@pytest.mark.parametrize("test_input,expected", [((5, 3, 8), 16), ((20.3, 30.1, 40.5), 90.9), ((0, 0.3), 0.3)])
def test_sumall_correct(test_input, expected):
    assert sum_all(*test_input) == expected


@pytest.mark.parametrize("test_input", [(1, 2, "str"), (1, (1, 2)), (None, [1, 2])])
def test_sumall_exception(test_input):
    with pytest.raises(TypeError):
        sum_all(test_input)


def test_timeof_day(freezer):
    frozen_time1 = datetime.datetime(
        2022, 2, 24, 8, 30, tzinfo=datetime.timezone.utc
    )
    freezer.move_to(frozen_time1)
    assert time_of_day() == "morning"
    frozen_time2 = datetime.datetime(
        1991, 2, 23, 20, 30, tzinfo=datetime.timezone.utc
    )
    freezer.move_to(frozen_time2)
    assert time_of_day() == "night"
