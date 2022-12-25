import queue
import socket
from threading import Thread
from time import sleep
import pytest

from client import Client


def test_init(test_urls_filename):
    n_threads = min(10, Client.MAX_THREADS)
    client = Client(n_threads, test_urls_filename)
    assert client._n_threads == n_threads
    client = Client(Client.MAX_THREADS + 10, test_urls_filename)
    assert client._n_threads == Client.MAX_THREADS


def test_read_urls(test_urls_filename):
    check = [
        'https://en.wikipedia.org/wiki/Georgia_State_Route_74',
        'https://en.wikipedia.org/wiki/Mediated_reference_theory',
        Client.THREAD_KILLER_TASK,
    ]
    client = Client(1, test_urls_filename)
    client._start_task_queue_constructor()
    client._stop_task_queue_constructor()

    urls = []
    while not client._task_queue.empty():
        urls.append(client._task_queue.get())

    assert urls == check


@pytest.mark.parametrize(
    "msg,port",
    [
        ('AlphaBravoCharlie', 7000),
        ('A' * Client.BUFFER_SIZE, 7001),
        ('A' * (3 * Client.BUFFER_SIZE), 7002),
        ('A' * (Client.BUFFER_SIZE + 1), 7003),
        ('A' * (Client.BUFFER_SIZE - 1), 7004),
    ]
)
def test_receive_data(msg, port):
    def simple_sender(host, port, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen()
            connection_socket, _ = sock.accept()
            msg += '\0'
            connection_socket.sendall(msg.encode('utf-8'))

    host = 'localhost'
    th_sender = Thread(target=simple_sender, args=(host, port, msg))
    th_sender.start()

    sleep(0.3)
    client = Client(1, None)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        received_msg = client._receive_data(sock)

    th_sender.join()
    assert received_msg == msg


def test_max_loaded_urls(file_with_10000_fake_urls):
    client = Client(1, file_with_10000_fake_urls)
    client._start_task_queue_constructor()
    sleep(0.3)
    assert client._task_queue.qsize() <= Client.MAX_TASKS_IN_QUEUE + 1
    while True:
        if client._task_queue.get() == Client.THREAD_KILLER_TASK:
            break
    client._stop_task_queue_constructor()
