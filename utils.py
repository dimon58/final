from time import perf_counter


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f'Function "{func.__name__}" completed in {end - start} sec')
        return result

    return wrapper
