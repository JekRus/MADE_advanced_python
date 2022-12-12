from multiprocessing import Process
import json
import requests_mock
import pytest

from client import Client
from server import Server


def test_init():
    n_threads = min(10, Server.MAX_THREADS)
    server = Server(n_threads, 5)
    assert server._n_threads == n_threads
    server = Server(Server.MAX_THREADS + 10, 5)
    assert server._n_threads == Server.MAX_THREADS


def test_process_query():
    server = Server(1, 5, timeout=2)
    url = 'https://test.com/test1'
    doc = '''
    <!DOCTYPE html>
    <html>
        <body>
            <h1>alpha bravo charlie!</h1>
            <p>alpha alpha, bravo;; delta Hotel foxtrot charlie@
            Echo delta delta1</p>
            <p>Hotel India</p>
        </body>
    </html>
    '''
    answer = {
        'alpha': 3, 'bravo': 2, 'charlie': 2, 'delta': 2, 'Hotel': 2
    }

    with requests_mock.Mocker() as mock:
        mock.get(url, text=doc)
        result = server._process_query(url)

    assert json.loads(result) == answer

    with requests_mock.Mocker() as mock:
        mock.get(url, status_code=404)
        result = server._process_query(url)

    assert result == 'Bad response.'

    result = server._process_query('htssds;/asds')
    assert result == 'Wrong format.'


def client_app(*args):
    client = Client(*args)
    client.run()


def server_app(*args):
    server = Server(*args, timeout=2)
    server.run()


def test_communication(test_urls_filename):
    th_client = Process(target=client_app, args=(1, test_urls_filename))
    th_server = Process(target=server_app, args=(10, 5))
    try:
        th_server.start()
        th_client.start()
        th_client.join()
        th_server.join()
    except Exception:
        pytest.fail("Unexpected Error")
