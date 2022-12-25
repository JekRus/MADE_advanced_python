import pytest


@pytest.fixture
def test_urls_filename():
    yield 'test_urls.txt'


@pytest.fixture
def file_with_10000_fake_urls(tmp_path):
    n_urls = 10_000
    sample_url = "https://fakeurl"
    fname = "tmp_urls.txt"
    tmp_file = tmp_path / fname
    with open(tmp_file, 'w') as f:
        for i in range(n_urls):
            f.write(f"{sample_url}_{i}\n")
    yield tmp_file
