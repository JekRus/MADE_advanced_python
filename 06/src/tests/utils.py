from typing import List
from pathlib import Path


def get_mocked_file_content(url: str) -> str:
    return f"response {url}"


def get_mocked_filename(url: str) -> str:
    return url.split("/")[-1]


def check_saved_files(
    directory: Path,
    expected_filenames: List[str],
    expected_contents: List[str],
):
    for filename, content in zip(expected_filenames, expected_contents):
        path = directory / filename
        assert path.exists()

        data = path.read_text()
        assert data == content
