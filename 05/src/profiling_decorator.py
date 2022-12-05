import cProfile
from functools import wraps


def profile_deco(func):
    profiler = cProfile.Profile()

    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        return result

    def print_stat():
        profiler.print_stats()

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


if __name__ == "__main__":
    add(1, 2)
    add(4, 5)
    add.print_stat()

    sub(1, 2)
    sub(4, 5)
    sub(10, 10)
    sub.print_stat()
