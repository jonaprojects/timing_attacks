import string
import time
from enum import Enum
import timeit


class Colors(Enum):
    """ A set of colors to print to the console """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


real_password = "Very secret password!"

# We would rather not handle special characters to save time in comparison
allowed_characters = string.ascii_letters + ' ' + string.digits


def compare_strings(string1: str, string2: str) -> bool:
    """ A custom string equality method that's vulnerable on purpose"""
    if len(string1) != len(string2):
        return False
    for char1, char2 in zip(string1, string2):
        if char1 != char2:
            return False
    return True


def print_guess(guess: str, index: int) -> None:
    print(Colors.OKGREEN.value + f"\r{guess[:index]}" + Colors.ENDC.value, end="", flush=True)
    print(guess[index:], end="", flush=True)


def login(password: str) -> bool:
    return compare_strings(password, real_password)


def crack_length(max_length=32, trials=1000):
    """ Crack the length of the real password by exploiting its behaviour"""
    times_elapsed = []

    print(Colors.UNDERLINE.value + "Cracking the length of the password..." + Colors.ENDC.value)
    dummy_string = "a"
    for i in range(max_length):
        current_time = timeit.repeat(lambda: login(dummy_string), repeat=10, number=trials)
        times_elapsed.append(current_time)
        dummy_string += "a"

    indices_range = range(len(times_elapsed))
    max_index = max(indices_range, key=lambda index: times_elapsed[index])
    password_length = max_index + 1

    print(f"The length is {password_length}")
    return password_length


def crack_password(trials=1000) -> tuple[str, bool]:
    password_length = crack_length()
    print(Colors.UNDERLINE.value + "Cracking the password..." + Colors.ENDC.value)

    current_guess = "_" * password_length

    for index in range(password_length):
        if login(current_guess):
            return current_guess, True

        max_guess = ''
        max_time_elapsed = 0

        for character in allowed_characters:
            next_guess = current_guess[:index] + character + current_guess[index + 1:]
            print_guess(next_guess, index)
            current_time = timeit.repeat(lambda: login(next_guess), repeat=75, number=trials)
            print_guess(current_guess, index)
            min_time = min(current_time)
            if min_time > max_time_elapsed:
                max_time_elapsed = min_time
                max_guess = next_guess

        current_guess = max_guess

    return current_guess, False


def main():
    result = crack_password()
    print(result)


if __name__ == '__main__':
    main()
