import argparse
import socket
import queue
import json
from typing import Union
from collections import Counter
from threading import Thread, Lock
from string import punctuation

import requests
from bs4 import BeautifulSoup

from logger import init_logger


logger = init_logger('logging_conf.yaml', 'server')


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Server',
        description='Downloads urls',
    )
    parser.add_argument('-w', type=int, action='store', dest='n_threads')
    parser.add_argument('-k', type=int, action='store', dest='n_top')
    return parser


class Server:
    BUFFER_SIZE = 4096
    MAX_THREADS = 500
    MAX_TASKS_IN_QUEUE = 1000
    THREAD_KILLER_TASK = '_STOP'

    def __init__(self, n_threads: int, n_top: int, host: str = 'localhost',
                 port: int = 5000, timeout: Union[int, None] = None):
        if n_threads > Server.MAX_THREADS:
            msg = 'Requested number of threads is too high.'\
                  ' Number of threads is set to %d.'
            logger.warning(msg, Server.MAX_THREADS)
            self._n_threads = Server.MAX_THREADS
        else:
            self._n_threads = n_threads
        self._host = host
        self._port = port
        self._n_top = n_top
        self._task_queue = queue.Queue(Server.MAX_TASKS_IN_QUEUE)
        self._lock = Lock()
        self._workers = None
        self._alive = True
        self._timeout = timeout
        self._task_counter = 0

    def run(self):
        logger.info('Start workers.')
        self._init_workers()
        logger.info('Start listening on port %d.', self._port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            if self._timeout:
                server_socket.settimeout(self._timeout)
            server_socket.bind((self._host, self._port))
            server_socket.listen()
            while self._alive:
                self._handle_client(server_socket)
        self._stop_workers()
        logger.info('Server stopped by timeout')

    def _init_workers(self):
        self._workers = [
            Thread(target=self._process_connections)
            for _ in range(self._n_threads)
        ]
        for worker in self._workers:
            worker.start()

    def _stop_workers(self):
        self._task_queue.put((None, Server.THREAD_KILLER_TASK))
        for worker in self._workers:
            worker.join()

    def _handle_client(self, server_socket):
        try:
            connection_socket, _ = server_socket.accept()
        except socket.timeout:
            self._alive = False
        else:
            url = connection_socket.recv(Server.BUFFER_SIZE).decode('utf-8')
            self._task_queue.put((connection_socket, url))

    def _process_connections(self):
        while True:
            connection_socket, url = self._task_queue.get()
            if url == Server.THREAD_KILLER_TASK:
                self._task_queue.put((None, url))
                return
            response = requests.get(url)
            if response.status_code != requests.status_codes.codes.ok:
                logger.error('Unable to process url %s', url)
                connection_socket.sendall(
                    json.dumps({'No data': -1}).encode('utf-8')
                )
                return
            soup = BeautifulSoup(response.text, features="html.parser")
            text = soup.get_text()
            text = text.translate(text.maketrans('', '', punctuation))
            word_counter = Counter(text.split())
            most_common_words = word_counter.most_common(self._n_top)
            result_msg = json.dumps(dict(most_common_words))
            connection_socket.sendall(result_msg.encode('utf-8'))
            with self._lock:
                self._task_counter += 1
                logger.info('Total processed: %d tasks', self._task_counter)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    logger.info('Start server application.')
    server = Server(args.n_threads, args.n_top)
    server.run()
