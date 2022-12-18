import pytest


@pytest.fixture
def valid_integer():
    yield 10


@pytest.fixture
def valid_string():
    yield 'Alpha'


@pytest.fixture
def valid_positive_integer():
    yield 1_000


@pytest.fixture
def valid_login():
    yield 'Alex12'


@pytest.fixture
def valid_password():
    yield 'wjs43P@5'
