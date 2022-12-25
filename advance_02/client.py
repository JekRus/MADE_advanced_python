import argparse
import json
import socket
import queue
from threading import Thread

from logger import init_logger


logger = init_logger('logging_conf.yaml', 'client')


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Client',
        description='Sends url downloading requests',
    )
    parser.add_argument('n_threads', type=int, action='store')
    parser.add_argument('filename', type=str, action='store')
    return parser


class Client:
    MAX_THREADS = 20
    BUFFER_SIZE = 4096
    MAX_TASKS_IN_QUEUE = 1000
    THREAD_KILLER_TASK = '_STOP'

    def __init__(self, n_threads: int, filename: str, host: str = 'localhost',
                 port: int = 5000):
        logger.info('Start client application.')
        if n_threads > Client.MAX_THREADS:
            msg = (
                'Requested number of threads is too high.'
                ' Number of threads is set to %d.'
            )
            logger.warning(msg, Client.MAX_THREADS)
            self._n_threads = Client.MAX_THREADS
        else:
            self._n_threads = n_threads
        self._filename = filename
        self._host = host
        self._port = port
        self._task_queue_constructor = None
        self._workers = None
        self._urls = None
        self._task_queue = None

    def run(self):
        logger.info('Start workers.')
        self._start_task_queue_constructor()
        self._start_workers()
        self._stop_workers()
        self._stop_task_queue_constructor()
        logger.info('Stop client application.')

    def _construct_task_queue(self):
        self._task_queue = queue.Queue(self.MAX_TASKS_IN_QUEUE + 1)
        with open(self._filename, 'r') as f:
            for line in f:
                self._task_queue.put(line.strip())
        self._task_queue.put(Client.THREAD_KILLER_TASK)

    def _start_task_queue_constructor(self):
        self._task_queue_constructor = Thread(target=self._construct_task_queue)
        self._task_queue_constructor.start()

    def _stop_task_queue_constructor(self):
        self._task_queue_constructor.join()

    def _start_workers(self):
        self._workers = [
            Thread(target=self._process_tasks) for _ in range(self._n_threads)
        ]
        for worker in self._workers:
            worker.start()

    def _stop_workers(self):
        for worker in self._workers:
            worker.join()

    def _receive_data(self, connection_socket):
        data = []
        chunk = connection_socket.recv(Client.BUFFER_SIZE).decode('utf-8')
        while not chunk.endswith('\0'):
            data.append(chunk)
            chunk = connection_socket.recv(Client.BUFFER_SIZE).decode('utf-8')
        data.append(chunk[:-1])
        data = ''.join(data)
        return data

    def _process_url(self, url):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self._host, self._port))
            msg = f'{url}\0'
            sock.sendall(msg.encode('utf-8'))
            response = self._receive_data(sock)
            try:
                result = json.loads(response)
            except json.decoder.JSONDecodeError:
                logger.warning('Bad response from server: %s', response)
            else:
                logger.info('%s: %s', url, result)

    def _process_tasks(self):
        while True:
            url = self._task_queue.get()
            if url == Client.THREAD_KILLER_TASK:
                self._task_queue.put(Client.THREAD_KILLER_TASK)
                return
            try:
                self._process_url(url)
            except Exception as e:
                logger.error(
                    'Unexpected error occurred while processing url. URL: %s; Exception: %s',
                    url,
                    str(e)
                )


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    client = Client(args.n_threads, args.filename)
    client.run()
