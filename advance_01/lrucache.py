import logging
from priority_queue import PriorityQueue


logger = logging.getLogger('LRUCache')


class LRUCache:
    def __init__(self, limit=42):
        self._storage = {}
        self._priority_queue = PriorityQueue()
        self._capacity = limit
        self._current_max_priority = -1
        logger.info("LRUCache created.")

    def get(self, key):
        if key in self._storage:
            self._current_max_priority += 1
            self._priority_queue.insert(key, self._current_max_priority)
            logger.info("Key=%s; value=%s.", key, self._storage[key])
            return self._storage[key]
        logger.warning("Key %s is not exist.", key)
        return None

    def set(self, key, value):
        if (
                (key not in self._storage)
                and (len(self._storage) == self._capacity)
        ):
            key_to_remove = self._priority_queue.pull()
            del self._storage[key_to_remove]
        self._storage[key] = value
        self._current_max_priority += 1
        self._priority_queue.insert(key, self._current_max_priority)
        logger.info("Key %s is set.", key)
