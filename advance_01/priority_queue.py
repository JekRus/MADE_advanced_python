#  The implementation idea is from the offical docs
#  https://docs.python.org/3/library/heapq.html

import heapq


class PriorityQueue:
    STATUS_FRESH = 1
    STATUS_STALE = 0

    def __init__(self):
        self._pqueue = []
        self._entry_finder = {}

    def _mark_stale(self, value):
        elem = self._entry_finder.pop(value)
        status = PriorityQueue.STATUS_STALE
        elem[-1] = status

    def is_empty(self) -> bool:
        return len(self._entry_finder) == 0

    def insert(self, value, priority: int):
        if value in self._entry_finder:
            self._mark_stale(value)
        status = PriorityQueue.STATUS_FRESH
        elem = [priority, value, status]
        self._entry_finder[value] = elem
        heapq.heappush(self._pqueue, elem)

    def pull(self):
        while len(self._pqueue) > 0:
            _, value, status = heapq.heappop(self._pqueue)
            if status:
                self._entry_finder.pop(value)
                return value
        raise IndexError("PriorityQueue is empty")

    def __len__(self):
        return len(self._entry_finder)
