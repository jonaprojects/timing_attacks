from matplotlib import pyplot as plt
from hmac import compare_digest
import timeit
import random
import string
from typing import Callable


def get_random_char():
    return random.choice(string.ascii_letters)


def generate_random_string(length: int):
    random_string = ''.join(get_random_char() for _ in range(length))
    return random_string


def measure_normal_equality(string1: str, string2: str) -> float:
    current_timings = timeit.repeat(lambda: string1 == string2, repeat=50, number=75)

    # return the min value to ignore background tasks and spikes in data
    return min(current_timings)


def measure_secure_equality(string1: str, string2: str) -> float:
    encoded1, encoded2 = string1.encode('utf-8'), string2.encode('utf-8')
    current_timings = timeit.repeat(lambda: compare_digest(encoded1, encoded2), repeat=50, number=75)

    # return the min value to ignore background tasks and spikes in data
    return min(current_timings)


def measure_equality_time(my_string: str, equality_measuring_method:Callable[[str, str], float]) -> list[float]:
    time_measures = []

    for mismatch_index in range(len(my_string)):

        # Make sure the character we're modifying is different
        if my_string[mismatch_index] == 'a':
            modified_char = 'b'
        else:
            modified_char = 'a'

        string_variant = my_string[:mismatch_index] + modified_char + my_string[mismatch_index + 1:]
        comparison_time = equality_measuring_method(my_string, string_variant)
        time_measures.append(comparison_time)

    return time_measures


def plot_time_measures(time_measures: list[float])->None:
    indices = [index for index in range(len(time_measures))]
    plt.plot(indices, time_measures)
    plt.xlabel("First mismatch index")
    plt.ylabel("Time to compare 75 times")
    plt.show()


def analyze_equality_time():
    """Analyze the string equality behavior depending on the first index of inequality"""
    random_string = generate_random_string(length=5000)
    time_measures = measure_equality_time(random_string, measure_secure_equality)
    plot_time_measures(time_measures)


def main():
    analyze_equality_time()


if __name__ == '__main__':
    main()
