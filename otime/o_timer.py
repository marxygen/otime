import random
import platform
import sys
import time
import otime.exceptions as exceptions


def O_time(func, n=0, top_n=10000, step=1000, args: list = None, raises=(), min_accuracy=0.8):
    """
    Runs a series of tests to determine function complexity in terms of big-O.
    Attempts to replicate and upscale the provided argument as n grows larger, measures the execution time
    and then tries to deduce the most appropriate complexity boundary using that data.

    :param func: Function or None - function to be tested. If none specified, and none was specified during
        instantiation, NoFunctionSpecified exception will be raised.

    :param n: 0-based index of `args` that must be changed as n grows larger. For example, if your function accepts
        a list and a value and then finds the index of the value in the list, specify `n=0`

    :param top_n: Max length of input parameter as n grows larger.

    :param step: step of values that the function will be rerun against.

    :param args: Arguments to be passed to the function
    :param raises: Tuple of exceptions (subclasses of BaseException) that this function might raise. Exceptions from
        that list are not handled and wrapped but printed out. This parameter is used so that if your function raises
        some exception AS A PART OF ITS JOB (for example, if no value was found in the list so you raise ValueError),
        test execution is not paused. Must be passed in AS A TUPLE!

    :param min_accuracy: Minimum acceptable accuracy

    Exceptions:
       NoFunctionSpecified - If no function has been specified
    """

    data = {}

    args = list(args)

    for ln in range(0, top_n + step, step):
        fuzzed = _get_fuzzed_list(origin=args[n], num=ln)
        args[n] = fuzzed
        try:
            print(f'\rRunning with {len(fuzzed)} parameters...', end='')
            _, elapsed = timefunc(func)(*args)
        except raises:
            exception = sys.exc_info()
            print(f'[{exception[0].__name__}] {exception[1]}')
        except TypeError as e:
            raise exceptions.InvalidParametersError(str(e)) from e
        else:
            data[ln] = elapsed

    print(' Done running.\n')

    total_time = sum(data.values())

    print(f'Total running time: {total_time}')

    # First, try to fit in a polynomial
    degree, accuracy = _regress(data, min_accuracy)


def _get_measuring_func():
    """Returns the platform-dependent timing function"""
    # https://stackoverflow.com/a/3444043
    if platform.system() == 'Linux':
        return time.time
    else:
        return time.perf_counter


def _get_fuzzed_list(origin: list, num: int = 10, values_range: tuple = (-100, 10000)):
    """
    Returns a new list populated with random values

    :param origin: Original list
    :param num: Number of random values to insert
    :param range: Range of random values that will be generated
    """
    origin = list(origin)
    for i in range(num):
        position = random.randint(0, len(origin))
        origin.insert(position, random.randint(*values_range))

    return origin


def _regress(results: dict, min_accuracy=0.8):
    """
    Tries to find polynomial regression degree that reasonably satisfies the data provided."

    :param results: Dictionary of results {<n> : <time>}
    :param min_accuracy: Mininum acceptable accuracy

    Returns:
        degree of polynomial or -1 if couldn't find matching one, accuracy or None, if no degree satisfies
    """

    ...


def timefunc(func):
    """
    A decorator to measure function running time. Attempts to use the most precise measuring function depending
    on the platform
    """

    def wrapper(*args, **kwargs):
        measurer = _get_measuring_func()
        start = measurer()
        result = func(*args, **kwargs)
        elapsed = measurer() - start
        return result, elapsed

    return wrapper
