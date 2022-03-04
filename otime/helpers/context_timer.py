from typing import Callable
from time import perf_counter
import sys


class Timer:
    """This class allows you to measure time that the code inside its context takes to run"""

    def __init__(self, counter: Callable = perf_counter, dest: Callable = sys.stdout):
        """Initialize timer class

        :param counter: Counter to use to measure time. Defaults to `time.perf_counter`
        :param dest: Destination to write result to. Must have `.write()` method
        """
        if not callable(counter):
            raise ValueError(f'Counter must be a callable, not {type(counter)}')
        self.counter = counter

        if not hasattr(dest, 'write'):
            raise ValueError(f'Destination must have a `.write()` method')
        self.dest = dest

        self.start = None
        self.end = None

    def __enter__(self):
        self.start = self.counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = self.counter()
        self.dest.write(str(self.end - self.start))
