from typing import Optional
from functools import partial
from contextlib import asynccontextmanager
from unittest.mock import Mock, patch
import asyncio

import pytest
import aiohttp

from fetcher import (
    fetch_url,
    save_html,
    coro_fetcher,
    main,
    STOP_TASK,
    RESPONSE_OK,
)
from .utils import get_mocked_file_content, get_mocked_filename, check_saved_files


class MockResponse:
    def __init__(self, url: str, ssl: bool, mocked_status: int):
        self.status = mocked_status
        self.url = url
        self.ssl = ssl

    async def text(self) -> Optional[str]:
        return get_mocked_file_content(self.url) if self.status == RESPONSE_OK else None


@asynccontextmanager
async def mock_get(url, mocked_status, ssl=True):
    yield MockResponse(url, ssl, mocked_status)


@pytest.mark.parametrize(
    "mocked_status,url",
    [
        (400, "url1"),
        (404, "url1"),
        (300, "url1"),
        (100, "url1"),
        (200, "url1"),
        (200, ""),
    ],
)
@pytest.mark.asyncio
async def test_fetch_url(mocked_status, url, monkeypatch):
    session = aiohttp.ClientSession()
    monkeypatch.setattr(session, "get", partial(mock_get, mocked_status=mocked_status))
    expected = get_mocked_file_content(url) if mocked_status == RESPONSE_OK else None
    assert await fetch_url(session, url) == expected


@pytest.mark.parametrize(
    "url,expected_exception",
    [
        (12, TypeError),
        (44.2, TypeError),
        (dict(), TypeError),
        ("invalidurl", aiohttp.client_exceptions.InvalidURL),
        ("https:/another/invalid/url", aiohttp.client_exceptions.InvalidURL),
    ],
)
@pytest.mark.asyncio
async def test_fetch_url_wrong_url(url, expected_exception):
    session = aiohttp.ClientSession()
    with pytest.raises(expected_exception):
        await fetch_url(session, url)


@pytest.mark.parametrize(
    "session,expected_exception",
    [
        (12, TypeError),
        (44.2, TypeError),
        (dict(), TypeError),
        ("some string", TypeError),
        ([1, 2, 3], TypeError),
    ],
)
@pytest.mark.asyncio
async def test_fetch_url_wrong_session(session, expected_exception):
    valid_url = "https://en.wikipedia.org/wiki/Mediated_reference_theory"
    with pytest.raises(expected_exception):
        await fetch_url(session, valid_url)


@pytest.mark.parametrize(
    "url,html",
    [
        ("https://en.wikipedia.org/wiki/Mediated_reference_theory", "HTML1_TEXT",),
        ("en.wikipedia.org/wiki/Mediated_reference_theory", "HTML1_TEXT",),
        ("1312url", "HTML1_TEXT"),
        ("1312url", "HTML2_TEXT"),
        ("1312url", ""),
    ],
)
@pytest.mark.asyncio
async def test_save_html(url, html, tmp_path):
    await save_html(url, html, tmp_path)

    expected_filename = get_mocked_filename(url)
    expected_content = html
    check_saved_files(tmp_path, [expected_filename], [expected_content])


@pytest.mark.parametrize(
    "url,html,expected_exception",
    [
        ("", "HTML1_TEXT", IsADirectoryError),
        (10, "HTML1_TEXT", AttributeError),
        (dict(), "HTML1_TEXT", AttributeError),
        ("valid_url", 12, TypeError),
        ("valid_url", dict(), TypeError),
        ("valid_url", 42.2, TypeError),
    ],
)
@pytest.mark.asyncio
async def test_save_html_wrong_arguments(url, html, expected_exception, tmp_path):
    with pytest.raises(expected_exception):
        await save_html(url, html, tmp_path)


@pytest.mark.asyncio
async def test_coro_fetcher(
    urls, expected_filenames, expected_contents, tmp_path, caplog
):
    task_queue = asyncio.Queue()
    for url in urls:
        await task_queue.put(url)
    await task_queue.put(STOP_TASK)

    with patch.object(
        aiohttp.ClientSession, "get", partial(mock_get, mocked_status=RESPONSE_OK)
    ):
        await coro_fetcher(task_queue, tmp_path)

    check_saved_files(tmp_path, expected_filenames, expected_contents)

    for log_msg in caplog.messages:
        assert log_msg.startswith("Task done")


@pytest.mark.asyncio
async def test_coro_fetcher_bad_response(urls, expected_filenames, tmp_path, caplog):
    BAD_RESPONSE = 400
    task_queue = asyncio.Queue()
    for url in urls:
        await task_queue.put(url)
    await task_queue.put(STOP_TASK)

    with patch.object(
        aiohttp.ClientSession, "get", partial(mock_get, mocked_status=BAD_RESPONSE)
    ):
        await coro_fetcher(task_queue, tmp_path)

    for url, expected_filename in zip(urls, expected_filenames):
        path = tmp_path / expected_filename
        assert not path.exists()

    for log_msg in caplog.messages:
        assert log_msg.startswith("Bad response")


@pytest.mark.parametrize("n_simultaneous_requests", [1, 2, 5, 7, 10, 20])
@pytest.mark.asyncio
async def test_main(
    n_simultaneous_requests,
    urls,
    expected_filenames,
    expected_contents,
    tmp_path,
    caplog,
):
    input_file = tmp_path / "test_urls.txt"
    input_file.write_text("\n".join(urls))

    args_mock = Mock(
        n_simultaneous_requests=n_simultaneous_requests,
        input_filename=str(input_file),
        output_dir_name=str(tmp_path),
    )

    with patch.object(
        aiohttp.ClientSession, "get", partial(mock_get, mocked_status=RESPONSE_OK)
    ):
        await main(args_mock)

    check_saved_files(tmp_path, expected_filenames, expected_contents)

    logged_tasks = [
        msg
        for msg in caplog.messages
        if msg.startswith("Bad response") or msg.startswith("Task done")
    ]
    total_logged_tasks = len(logged_tasks)
    assert total_logged_tasks == len(urls)
