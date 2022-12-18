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


def test_basic_valid_values(
        valid_integer,
        valid_string,
        valid_positive_integer,
        valid_login,
        valid_password,
):
    Data(valid_integer, valid_string, valid_positive_integer)
    User(valid_login, valid_password)


@pytest.mark.parametrize(
    'num',
    [-100, -44, -1, 0, 1, 10, 33, 2312],
)
def test_integer_basic(
        valid_integer, valid_string, valid_positive_integer, num
):
    data_instance = Data(valid_integer, valid_string, valid_positive_integer)

    data_instance.num = num
    Data(num, valid_string, valid_positive_integer)


@pytest.mark.parametrize(
    'name',
    ['Qwe', 'aaaab', 'cklkl', '123', '!!!', ''],
)
def test_string_basic(
        valid_integer, valid_string, valid_positive_integer, name
):
    data_instance = Data(valid_integer, valid_string, valid_positive_integer)

    data_instance.name = name
    Data(valid_integer, name, valid_positive_integer)


@pytest.mark.parametrize(
    'num',
    [
        'alpha',
        [1, 2, 3],
        12.5,
        set(),
        {'a': 1, 'b': 2},
    ]
)
def test_type_checks_integer(
        valid_integer, valid_string, valid_positive_integer, num
):
    data_instance = Data(valid_integer, valid_string, valid_positive_integer)

    with pytest.raises(TypeError):
        data_instance.num = num
    with pytest.raises(TypeError):
        Data(num, valid_string, valid_positive_integer)


@pytest.mark.parametrize(
    'name',
    [
        10,
        [1, 2, 3],
        12.5,
        set(),
        {'a': 1, 'b': 2},
    ]
)
def test_type_checks_string(
        valid_integer, valid_string, valid_positive_integer, name
):
    data_instance = Data(valid_integer, valid_string, valid_positive_integer)

    with pytest.raises(TypeError):
        data_instance.name = name
    with pytest.raises(TypeError):
        Data(valid_integer, name, valid_positive_integer)


@pytest.mark.parametrize(
    'price',
    [
        'alpha',
        [1, 2, 3],
        12.5,
        set(),
        {'a': 1, 'b': 2},
    ]
)
def test_type_checks_positive_integer(
        valid_integer, valid_string, valid_positive_integer, price
):
    data_instance = Data(valid_integer, valid_string, valid_positive_integer)

    with pytest.raises(TypeError):
        data_instance.price = price
    with pytest.raises(TypeError):
        Data(valid_integer, valid_string, price)


@pytest.mark.parametrize(
    'login',
    [
        10,
        [1, 2, 3],
        12.5,
        set(),
        {'a': 1, 'b': 2},
    ]
)
def test_type_checks_login(valid_login, valid_password, login):
    user_instance = User(valid_login, valid_password)

    with pytest.raises(TypeError):
        user_instance.login = login
    with pytest.raises(TypeError):
        User(login, valid_password)


@pytest.mark.parametrize(
    'password',
    [
        10,
        [1, 2, 3],
        12.5,
        set(),
        {'a': 1, 'b': 2},
    ]
)
def test_type_checks_password(valid_login, valid_password, password):
    user_instance = User(valid_login, valid_password)

    with pytest.raises(TypeError):
        user_instance.password = password
    with pytest.raises(TypeError):
        User(valid_login, password)


@pytest.mark.parametrize(
    'price,is_valid',
    [
        (-100, False),
        (-423, False),
        (0, False),
        (100, True),
        (1, True),
        (24, True),
        (1_000_000_000, True),
    ]
)
def test_positive_integer(valid_positive_integer, price, is_valid):
    data_instance = Data(1, 'alpha', valid_positive_integer)

    if is_valid:
        data_instance.price = price
        Data(1, 'alpha', price)
    else:
        with pytest.raises(ValueError):
            data_instance.price = price
        with pytest.raises(ValueError):
            Data(1, 'alpha', price)


@pytest.mark.parametrize(
    'name,is_valid',
    [
        ('Alex', False),
        ('VeryLongName', False),
        ('AnotherLongName', False),
        ('Jordan', True),
        ('Igorek', True),
        ('Petya', True),
        ('X Æ A-12', True),
    ]
)
def test_string_len_constraints(name, is_valid):
    class Data2:
        num = Integer()
        name = String(min_len=5, max_len=10)
        price = PositiveInteger()

        def __init__(self, num, name, price):
            self.num = num
            self.name = name
            self.price = price

    basic_valid_name = 'Vladimir'
    data2_instance = Data2(1, basic_valid_name, 100)

    if is_valid:
        data2_instance.name = name
        Data2(1, name, 100)
    else:
        with pytest.raises(ValueError):
            data2_instance.name = name
        with pytest.raises(ValueError):
            Data2(1, name, 100)


@pytest.mark.parametrize(
    'login,is_valid',
    [
        ('ABC', True),
        ('Alexaaaaaaaaaaaandr', True),
        ('Alex', True),
        ('Killer666', True),
        ('xXxMonsterxXx', True),
        ('ProstoVasya', True),

        ('aa', False),  # too short
        ('Alexaaaaaaaaaaaaaaaaaaaaa', False),  # too long
        ('Alex!!', False),  # prohibited chars
        ('12Alex', False),  # begins with digit
    ]
)
def test_login(valid_login, valid_password, login, is_valid):
    user_instance = User(valid_login, valid_password)

    if is_valid:
        user_instance.login = login
        User(login, valid_password)
    else:
        with pytest.raises(ValueError):
            user_instance.login = login
        with pytest.raises(ValueError):
            User(login, valid_password)


@pytest.mark.parametrize(
    'password,is_valid',
    [
        ('w43P@5ed', True),
        ('ABCDE5!h', True),
        ('HHHHHh+1', True),
        ('qweRty96=', True),
        ('?!@#_%^4aW', True),

        ('w43P@5', False),    # too short
        ('wjs43P35', False),  # no special char
        ('wjs43p@5', False),  # no upper case
        ('WJS43P@5', False),  # no lower case
    ]
)
def test_password(valid_login, valid_password, password, is_valid):
    user_instance = User(valid_login, valid_password)

    if is_valid:
        user_instance.password = password
        User(valid_login, password)
    else:
        with pytest.raises(ValueError):
            user_instance.password = password
        with pytest.raises(ValueError):
            User(valid_login, password)
