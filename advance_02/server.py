import argparse
import socket
import queue
import json
import re
from typing import Union, Dict
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


class HTMLParser:
    def __init__(self, doc: str):
        self.doc = doc

    def get_text(self) -> str:
        soup = BeautifulSoup(self.doc, features="html.parser")
        text = soup.get_text()
        text = text.translate(text.maketrans('', '', punctuation))
        return text

    def get_top_words(self, n_top: int) -> Dict[str, int]:
        text = self.get_text()
        words = text.split()
        most_common_words = dict(Counter(words).most_common(n_top))
        return most_common_words


class Server:
    BUFFER_SIZE = 4096
    MAX_THREADS = 500
    MAX_TASKS_IN_QUEUE = 1000
    THREAD_KILLER_TASK = '_STOP'

    def __init__(self, n_threads: int, n_top: int, host: str = 'localhost',
                 port: int = 5000, timeout: Union[int, None] = None):
        logger.info('Start server application.')
        if n_threads > Server.MAX_THREADS:
            msg = (
                'Requested number of threads is too high.'
                ' Number of threads is set to %d.'
            )
            logger.warning(msg, Server.MAX_THREADS)
            self._n_threads = Server.MAX_THREADS
        else:
            self._n_threads = n_threads
        self._host = host
        self._port = port
        self._n_top = n_top
        self._timeout = timeout
        self._task_queue = queue.Queue(Server.MAX_TASKS_IN_QUEUE)
        self._workers = None
        self._alive = True
        self._task_counter = 0
        self._task_counter_lock = Lock()

    def run(self):
        logger.info('Start workers.')
        self._start_workers()
        logger.info('Start listening on port %d.', self._port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            if self._timeout:
                server_socket.settimeout(self._timeout)
            server_socket.bind((self._host, self._port))
            server_socket.listen()
            while self._alive:
                try:
                    conn_socket, address = server_socket.accept()
                except socket.timeout:
                    self._alive = False
                else:
                    self._task_queue.put((conn_socket, address))
        self._stop_workers()
        logger.info('Server stopped by timeout')

    def _start_workers(self):
        self._workers = [
            Thread(target=self._handle_connections)
            for _ in range(self._n_threads)
        ]
        for worker in self._workers:
            worker.start()

    def _stop_workers(self):
        self._task_queue.put((Server.THREAD_KILLER_TASK, None))
        for worker in self._workers:
            worker.join()

    def _receive_data(self, connection_socket: socket.socket) -> str:
        data = []
        chunk = connection_socket.recv(Server.BUFFER_SIZE).decode('utf-8')
        while not chunk.endswith('\0'):
            data.append(chunk)
            chunk = connection_socket.recv(Server.BUFFER_SIZE).decode('utf-8')
        data.append(chunk[:-1])
        data = ''.join(data)
        return data

    def _process_query(self, url: str) -> str:
        url_regex = re.compile(
            r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.'
            r'([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
        )
        if not re.match(url_regex, url):
            status = 'Wrong format.'
            logger.warning('Unable to process url %s. %s', url, status)
            return status
        response = requests.get(url)
        if response.status_code != requests.status_codes.codes.ok:
            status = 'Bad response.'
            logger.warning('Unable to process url %s. %s', url, status)
            return status
        most_common_words = (
            HTMLParser(response.text)
            .get_top_words(self._n_top)
        )
        result_msg = json.dumps(dict(most_common_words))
        return result_msg

    def _process_client(self, connection_socket: socket.socket):
        url = self._receive_data(connection_socket)
        result_msg = self._process_query(url)
        result_msg += '\0'
        connection_socket.sendall(result_msg.encode('utf-8'))
        with self._task_counter_lock:
            self._task_counter += 1
            logger.info('Total processed: %d tasks', self._task_counter)

    def _handle_connections(self):
        while True:
            connection_socket, address = self._task_queue.get()
            if connection_socket == Server.THREAD_KILLER_TASK:
                self._task_queue.put((Server.THREAD_KILLER_TASK, address))
                return
            try:
                self._process_client(connection_socket)
            except Exception as e:
                logger.error(
                    'Unexpected error occurred while processing client. '
                    'Client address: %s; Exception: %s',
                    address,
                    str(e)
                )


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    server = Server(args.n_threads, args.n_top, timeout=5)
    server.run()
