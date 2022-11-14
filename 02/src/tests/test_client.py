import queue

from client import Client


def test_init():
    n_threads = min(10, Client.MAX_THREADS)
    client = Client(n_threads, '../data/test_urls.txt')
    assert client._n_threads == n_threads
    client = Client(Client.MAX_THREADS + 10, '../data/test_urls.txt')
    assert client._n_threads == Client.MAX_THREADS


def test_read_urls():
    check = [
        'https://en.wikipedia.org/wiki/Georgia_State_Route_74',
        'https://en.wikipedia.org/wiki/Mediated_reference_theory'
    ]
    client = Client(1, '../data/test_urls.txt')
    client._read_urls()

    assert client._urls == check


def test_construct_task_queue():
    client = Client(1, '../data/test_urls.txt')
    client._read_urls()
    client._construct_task_queue()
    res_queue = client._task_queue
    ref_queue = queue.Queue(3)
    ref_queue.put('https://en.wikipedia.org/wiki/Georgia_State_Route_74')
    ref_queue.put('https://en.wikipedia.org/wiki/Mediated_reference_theory')
    ref_queue.put(client.THREAD_KILLER_TASK)
    assert res_queue.qsize() == ref_queue.qsize()
    for i in range(res_queue.qsize()):
        assert res_queue.get() == ref_queue.get()
