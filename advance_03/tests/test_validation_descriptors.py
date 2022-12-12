import pytest
from validation_descriptors import (
    Integer, PositiveInteger, String, Login, Password
)


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price


class User:
    login = Login(min_len=3, max_len=20)
    password = Password(min_len=8)

    def __init__(self, login, password):
        self.login = login
        self.password = password


def test_simple():
    data = Data(-5, 'alpha', 1_000)

    assert data.num == -5
    assert data.name == 'alpha'
    assert data.price == 1_000

    user = User('Alex', 'wjs43P@5')

    assert user.login == 'Alex'
    assert user.password == 'wjs43P@5'


def test_type_checks():
    with pytest.raises(TypeError):
        Data('alpha', 'bravo', 1_000)
    with pytest.raises(TypeError):
        Data([1, 2, 3], 'bravo', 1_000)
    with pytest.raises(TypeError):
        Data(12.5, 'bravo', 1_000)
    with pytest.raises(TypeError):
        Data(1, 5, 1_000)
    with pytest.raises(TypeError):
        Data(1, 'bravo', 'charlie')
    with pytest.raises(TypeError):
        User('zzz', [1, 2, 3])
    with pytest.raises(TypeError):
        User(12, 'zzz')


def test_positive_integer():
    with pytest.raises(ValueError):
        Data(1, 'alpha', -100)
    with pytest.raises(ValueError):
        Data(1, 'alpha', 0)


def test_string_len_constraints():
    class Data2:
        num = Integer()
        name = String(min_len=5, max_len=10)
        price = PositiveInteger()

        def __init__(self, num, name, price):
            self.num = num
            self.name = name
            self.price = price

    Data2(1, 'Vladimir', 100)

    with pytest.raises(ValueError):
        Data2(1, 'qqqq', 100)
    with pytest.raises(ValueError):
        Data2(1, 'qqqqqqqqqqq', 100)


def test_login():
    User('Alex12', 'wjs43P@5')

    with pytest.raises(ValueError):
        # too short
        User('aa', 'wjs43P@5')
    with pytest.raises(ValueError):
        # too long
        User('Alexaaaaaaaaaaaaaaaaaaaaa', 'wjs43P@5')
    with pytest.raises(ValueError):
        # prohibited chars
        User('Alex!!', 'wjs43P@5')
    with pytest.raises(ValueError):
        # begins with digit
        User('12Alex', 'wjs43P@5')


def test_password():
    User('Alex12', 'wjs43P@5')

    with pytest.raises(ValueError):
        # too short
        User('Alex12', 'w43P@5')
    with pytest.raises(ValueError):
        # no special char
        User('Alex12', 'wjs43P35')
    with pytest.raises(ValueError):
        # no upper case
        User('Alex12', 'wjs43p@5')
    with pytest.raises(ValueError):
        # no lower case
        User('Alex12', 'WJS43P@5')
