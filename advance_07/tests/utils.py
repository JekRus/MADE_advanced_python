import string


def atoi(inp: str, base: int) -> int:
    if not isinstance(inp, str):
        raise TypeError(
            f"Parameter 'string' must be str, got {type(inp).__name__} instead."
        )
    if not isinstance(base, int):
        raise TypeError(
            f"Parameter 'base' must be int, got {type(base).__name__} instead."
        )
    if base <= 1:
        raise ValueError("Parameter 'base' must be greater then 1.")

    result = 0
    digits = set("0123456789")
    alphabet = string.ascii_lowercase
    letters = dict(zip(alphabet, range(10, 37)))
    inp = inp.lower()
    idx = 0
    sign = 1
    if inp[0] in {"-", "+"}:
        sign = 1 if inp[0] == "+" else -1
        idx = 1
    for char in inp[idx:]:
        digit = ord(char) - ord("0") if char in digits else letters[char]
        result = result * base + digit
    result *= sign
    return result
