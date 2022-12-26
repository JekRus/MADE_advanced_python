import pytest


@pytest.mark.parametrize(
    "test_string,sep,exp_answer",
    [
        ("some/string", "/", ("some", "/", "string")),
        ("digit1sep1", "1", ("digit", "1", "sep1")),
        ("repeated/sep/in/str", "/", ("repeated", "/", "sep/in/str")),
        ("no sep", "/", ("no sep", "", "")),
        ("long_/_sep", "_/_", ("long", "_/_", "sep")),
        ("whole_string_is_sep", "whole_string_is_sep", ("", "whole_string_is_sep", "")),
        ("sepsep", "sep", ("", "sep", "sep")),
        ("sesepsep", "sep", ("se", "sep", "sep")),
        ("sepsepse", "sep", ("", "sep", "sepse")),
        ("//", "/", ("", "/", "/")),
        ("sep_at_leftsuffix", "sep_at_left", ("", "sep_at_left", "suffix")),
        ("prefixsep_at_right", "sep_at_right", ("prefix", "sep_at_right", "")),
    ],
)
def test_partition_basic(test_string, sep, exp_answer):
    assert test_string.partition(sep) == exp_answer


@pytest.mark.parametrize(
    "test_string",
    [
        "some/string",
        "digit1sep1",
        "QJMDQlkfsdkl",
        "\t\n \t\t",
    ],
)
def test_self_partition(test_string):
    assert test_string.partition(test_string) == ("", test_string, "")


@pytest.mark.parametrize(
    "sep", [42, range(10), [1, 2, 3], {"a": 1, "b": 2}, 44.0, {2, 3}, ("a", "b", "c")]
)
def test_partition_wrong_argument(sep):
    test_string = "test_string"
    with pytest.raises(TypeError):
        test_string.partition(sep)


def test_empty_sep():
    test_string = "test_string"
    with pytest.raises(ValueError):
        test_string.partition("")
