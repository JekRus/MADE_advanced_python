import pytest


@pytest.fixture
def test_urls_filename():
    yield 'test_urls.txt'
