import pytest

from .utils import atoi


@pytest.mark.parametrize(
    "inp,expected_output",
    [
        (1, 1),
        (34, 34),
        (0, 0),
        (-100, -100),
        (10.0, 10),
        (10.2, 10),
        (10.7, 10),
        ("0", 0),
        ("10", 10),
        ("-123", -123),
        ("1_000_000", 1000000),
        ("1_000_000_000_000_000_000_000_000", 1_000_000_000_000_000_000_000_000),
        ("-1_000_000_000_000_000_000_000_000", -1_000_000_000_000_000_000_000_000),
        (bytes(b"0"), 0),
        (bytes(b"10"), 10),
        (bytes(b"-127"), -127),
        (bytes(b"123"), 123),
        (bytearray(b"0"), 0),
        (bytearray(b"10"), 10),
        (bytearray(b"-127"), -127),
        (bytearray(b"123"), 123),
    ],
)
def test_int_basic(inp, expected_output):
    assert int(inp) == expected_output


def test_int_default():
    default_val = 0
    assert int() == default_val


@pytest.mark.parametrize(
    "inp,expected_exception",
    [
        (5 + 0j, TypeError),
        ([1, 2, 3], TypeError),
        (set(), TypeError),
        ({"a": 1, "b": 2}, TypeError),
        (range(10), TypeError),
        ([1, 2, 3], TypeError),
        ("12A", ValueError),
        ("abcd", ValueError),
        ("", ValueError),
        (bytes(b"12A"), ValueError),
        (bytes(b"abcd"), ValueError),
        (bytes(b""), ValueError),
        (bytearray(b"12A"), ValueError),
        (bytearray(b"abcd"), ValueError),
        (bytearray(b""), ValueError),
    ],
)
def test_int_wrong_argument(inp, expected_exception):
    with pytest.raises(expected_exception):
        int(inp)


@pytest.mark.parametrize(
    "inp_val,base,exp_out",
    [
        ("10", 10, 10),
        ("0", 10, 0),
        ("-127", 10, -127),
        ("0", 2, 0),
        ("1", 2, 1),
        ("10", 2, 2),
        ("100", 2, 4),
        ("101101", 2, 45),
        ("0B101101", 2, 45),
        ("0b101101", 0, 45),
        ("-101101", 2, -45),
        ("0", 8, 0),
        ("1", 8, 1),
        ("10", 8, 8),
        ("100", 8, 64),
        ("101101", 8, 33345),
        ("0o101101", 8, 33345),
        ("0o101101", 0, 33345),
        ("-101101", 8, -33345),
        ("0", 16, 0),
        ("0x0", 16, 0),
        ("0x0", 0, 0),
        ("1", 16, 1),
        ("10", 16, 16),
        ("100", 16, 256),
        ("A", 16, 10),
        ("B", 16, 11),
        ("C", 16, 12),
        ("D", 16, 13),
        ("E", 16, 14),
        ("F", 16, 15),
        ("a", 16, 10),
        ("b", 16, 11),
        ("c", 16, 12),
        ("d", 16, 13),
        ("e", 16, 14),
        ("f", 16, 15),
        ("0xA", 16, 10),
        ("0xA", 0, 10),
        ("0XA", 16, 10),
        ("0XA", 0, 10),
        ("0x3FD23", 0, 261411),
    ],
)
def test_int_base_manual(inp_val, base, exp_out):
    assert int(inp_val, base) == exp_out


@pytest.mark.parametrize(
    "inp_val,base",
    [
        ("0", 10),
        ("10", 10),
        ("1243", 10),
        ("-1321", 10),
        ("11011", 2),
        ("1111111", 2),
        ("1010101001", 2),
        ("0000100110", 2),
        ("11001100101", 2),
        ("53257", 8),
        ("7", 8),
        ("-32374", 8),
        ("125", 8),
        ("A", 16),
        ("A8DF", 16),
        ("-56E2A", 16),
        ("5F3DAB", 16),
        ("10212021212", 3),
        ("2222222221212", 3),
        ("12312332312312", 4),
        ("33212", 4),
        ("12124423", 5),
        ("444", 5),
        ("2212", 6),
        ("5", 6),
        ("10", 6),
        ("P55", 26),
        ("347HJASJ", 30),
        ("12ZZQWEXJY", 36),
        ("-Z1", 36),
    ],
)
def test_int_base_atoi(inp_val, base):
    assert int(inp_val, base) == atoi(inp_val, base)
