import pytest
from multiprocessing import Process
from client import Client
from server import Server


def test_init():
    n_threads = min(10, Server.MAX_THREADS)
    server = Server(n_threads, 5)
    assert server._n_threads == n_threads
    server = Server(Server.MAX_THREADS + 10, 5)
    assert server._n_threads == Server.MAX_THREADS


def client_app(*args):
    client = Client(*args)
    client.run()


def server_app(*args):
    server = Server(*args, timeout=2)
    server.run()


def test_communication():
    th_client = Process(target=client_app, args=(1, '../data/test_urls.txt'))
    th_server = Process(target=server_app, args=(10, 5))
    try:
        th_server.start()
        th_client.start()
        th_client.join()
        th_server.join()
    except Exception:
        pytest.fail("Unexpected Error")
