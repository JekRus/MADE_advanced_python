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
    THREAD_KILLER_TASK = '_STOP'

    def __init__(self, n_threads: int, filename: str, host: str = 'localhost',
                 port: int = 5000):
        if n_threads > Client.MAX_THREADS:
            msg = 'Requested number of threads is too high.' \
                  ' Number of threads is set to %d.'
            logger.warning(msg, Client.MAX_THREADS)
            self._n_threads = Client.MAX_THREADS
        else:
            self._n_threads = n_threads
        self._filename = filename
        self._host = host
        self._port = port
        self.workers = None
        self._urls = None
        self._task_queue = None

    def run(self):
        self._read_urls()
        self._construct_task_queue()
        self.workers = [
            Thread(target=self._process_tasks) for _ in range(self._n_threads)
        ]
        for worker in self.workers:
            worker.start()
        for worker in self.workers:
            worker.join()

    def _read_urls(self):
        with open(self._filename, 'r') as f_in:
            self._urls = [url.strip() for url in f_in.readlines()]

    def _construct_task_queue(self):
        self._task_queue = queue.Queue(len(self._urls) + 1)
        for url in self._urls:
            self._task_queue.put(url)
        self._task_queue.put(Client.THREAD_KILLER_TASK)

    def _recieve_json(self, r_socket: socket.socket):
        rec_data = bytes()
        result = None
        while not result:
            try:
                rec_data += r_socket.recv(Client.BUFFER_SIZE)
                result = json.loads(rec_data.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                pass
            except socket.error as e:
                logger.error(str(e))
        return result

    def _process_tasks(self):
        while True:
            url = self._task_queue.get()
            if url == Client.THREAD_KILLER_TASK:
                self._task_queue.put(url)
                return
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self._host, self._port))
                sock.sendall(url.encode('utf-8'))
                result = self._recieve_json(sock)
                logger.info('%s: %s', url, result)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    logger.info('Start client application.')
    client = Client(args.n_threads, args.filename)
    client.run()

    logger.info('Stop client application.')
