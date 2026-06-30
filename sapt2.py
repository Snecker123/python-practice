"""
Ex 1:
Write a function that prints numbers from 1 to 10.
"""
from functools import reduce
from random import randrange


def print_one_to_ten():
    print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])



print_one_to_ten()

"""
Ex 2:
Write a function that returns the sum of all numbers from 1 to n.
Example: input 5 should return 15 (1+2+3+4+5)
"""

def sum_n(n):
    numbers = []
    for i in range(1, n):
        numbers.append(i)
    return sum(numbers)


"""
Ex 3:
Write a function that takes a list of numbers and returns only the even numbers.
Example: input [1, 2, 3, 4, 5, 6] should return [2, 4, 6]
"""

def sort_even_numbers(list):
    return sorted(list, key=lambda n: n % 2 == 0)

"""
Ex 4:
Write a function that reverses a string and returns a list with each letter.
Example: input "hello" should return ["o", "l", "l", "e", "h"]
"""


def reverse(string):
    return sorted(string, reverse = True)


"""
Ex 5:
Write a function that counts the number of vowels in a string.
Example: input "hello world" should return 3
"""


def count_vowels(string):
    return len(list(filter(lambda x: x in "aeiouAEIOU", string)))

print(count_vowels("hello world"))


"""
Ex 6:
Write a function that finds the maximum number in a list.
Example: input [3, 7, 2, 9, 1] should return 9
"""

def find_max(ls):
    # return max(ls)
    maximum = min(ls)
    for i in ls:
        if i > maximum:
            maximum = i

    return maximum


"""
Ex 7:
Implement a search to find the index of a target value in a sorted list.
Return -1 if not found.
Example: input search_list=[1, 3, 5, 7, 9, 11], value=7 should return 3
"""


def search_index(search_list, value) -> int:
    st = 0
    dr = len(search_list) - 1

    # Condiția <= asigură că verificăm și listele cu 1 singur element
    while st <= dr:
        mij = (st + dr) // 2  # Se calculează mereu aici

        if search_list[mij] == value:
            return mij
        elif search_list[mij] < value:
            st = mij + 1  # Eliminăm mijlocul, căutăm la dreapta
        else:
            dr = mij - 1  # Eliminăm mijlocul, căutăm la stânga

    return -1


"""
Ex 8:
Write a function that prints the multiplication table for a given number n.
Example: exercise_8(3) should print:
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
... up to 3 x 10 = 30
"""

def exercise_8(n):
    for i in range(1, 11):
        print(f"{i} x {n} = {i*n}\n")


# exercise_8(10)

"""
Ex 9:
Write a function that calculates the factorial of a number.
Example: input=5 should return 120 (5*4*3*2*1)
"""

def factorial(n:int) -> int:
    return reduce(lambda x, y: x * y, range(1, n+1), 1)

"""
Ex 10:
Write a function that checks if a number is prime.
Example: input=17 should return True, is_prime(15) should return False
"""

def is_prime(n:int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    elif n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

"""
Ex 11:
Write a function that removes duplicates from a list while preserving order.
Example: input=[1, 2, 2, 3, 4, 4, 5] should return [1, 2, 3, 4, 5]
"""
def remove_duplicates(ls:list[int]) -> list[int]:
    return list(dict.fromkeys(ls))

# print(remove_duplicates([1, 2, 2, 3, 4, 4, 5]))

"""
Ex 12:
Write a function that implements a Caesar cipher (shifts each letter by n positions).
You can search for ord and chr functions to help with character shifting.
ord - converts a Unicode character to its corresponding integer Unicode code point value.
chr - converts an integer Unicode code point value back to its corresponding character.
Example: input_str="abc", value=2 should return "cde"
"""

def caesar_cipher(input_str:str, value:int) -> str:
    output = ""
    for i in input_str:
        output = output + (chr(ord(i) + value))
    return output
# print(caesar_cipher(input_str="abc", value=2))

"""
Ex 13:
Write a function that generates the first n numbers in the Fibonacci sequence.
Example: input=7 should return [0, 1, 1, 2, 3, 5, 8]
"""
def fibonacci_seq(n:int) -> list[int]:
    numbers = [0, 1, 1]
    if n == 1:
        return [0]
    elif n == 2:
        return [1]
    elif n == 3:
        return numbers
    elif n > 3:
        for i in range(2, n):
            numbers.append(numbers[i - 1] + numbers[i - 2])
    else:
        return []
    return numbers

"""
Ex 14:
Write a function that checks if a string is a palindrome (ignoring spaces and case).
Example: input="A man a plan a canal Panama" should return True
"""

def if_palindrome(string:str) -> bool:
    if sorted(string, reverse = True) == string:
        return True
    return False

"""
Ex 15:
Given a text, count how many times each letter appears.
Given large enough text, is there a difference between english and romanian texts?
"""
def letter_count(text:str):
    alphabet = ord('z') - ord('a')
    for i in range(0, alphabet+1):
        nr = text.lower().count(   chr(  i + ord('a') )   )
        print(f"{chr(  i + ord('a') )} = {nr}\n")

# letter_count("aaAaAaa")


"""Ex 16:
Generate 1000 unique latitude and longitude coordinates of type (x,y), should be integers, x between -90 and 90, y between -180 and 180.
Find and print the closest two points and the farthest two points.
"""

def find_closest() -> int:
    x = []
    y = []
    for i in range(1, 1000):
        x.append(randrange(-90, 91))
        y.append(randrange(-180, 181))
