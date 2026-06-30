# This is a sample Python script.
import random
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


"""Problem 1: Password Strength Checker
Write a function check_password_strength(password) that checks if a given password is strong.
A strong password:
 - is at least 8 characters long
 -  contains at least one uppercase letter,
 - one lowercase letter
 - and one number.
Return "Strong" if it meets the criteria or "Weak" otherwise.

Example:
Python123 ➔ "Strong"
weakpass ➔ "Weak"
"""
def check_password_strength(password):
    if len(password) < 8 :
        return "Weak"
    elif password == password.lower():
        return "Weak"
    elif password == password.upper():
        return "Weak"

    for i in password:
        if i.isdigit():
            return "Strong"

    return "Weak"



"""
Problem 2: Guess the Number (with Exception Handling)
Write a program that asks the user to guess a secret number between 1 and 10.
The program should handle invalid inputs (non-numeric values) gracefully using
try/except and print helpful error messages.
The game ends when the user guesses the correct number.

Example:
Enter your guess: abc ➔ Invalid input. Please enter a number.
Enter your guess: 5 ➔ Too low!
Enter your guess: 10 ➔ Too high!
Enter your guess: 8 ➔ Correct! You win! """

def guess_the_number():
    # Generate a secret number between 1 and 10
    secret_number = random.randint(1, 10)

    print("I am thinking of a number between 1 and 10.")

    while True:
        try:
            # Get input from the user
            user_input = input("Enter your guess: ")

            # Try to convert the input to an integer
            guess = int(user_input)

            # Check the guess against the secret number
            if guess < secret_number:
                print("➔ Too low!")
            elif guess > secret_number:
                print("➔ Too high!")
            else:
                print("➔ Correct! You win!")
                break  # Exit the loop and end the game

        except ValueError:
            # Handle the error if the input cannot be converted to an integer
            print("➔ Invalid input. Please enter a number.")


"""
 Problem 3: Temperature Logger (Read/Write File)
Write two functions:

 - log_temperature(temp) ➔ Appends the temperature to a file named "temperatures.txt".
 - read_temperatures() ➔ Reads all temperatures from the file and prints the average temperature

Example:
log_temperature(25) -> saves 25 in file
log_temperature(30) -> saves 30 in file
read_temperatures() ➔ Average temperature: 27.5°C """

def log_temperatures(temp):
    try:
        with open("temperatures.txt", "a") as file:
            file.write(f"{temp}\n")
    except Exception as e:
        print(e)

def read_temperatures():
    temperaturi = []
    try:
        with open("Temperatures.txt", "r") as file:
            for line in file:
                line = line.strip()
                temperaturi.append(float(line))
    except Exception as e:
        print (e)
        return

    if temperaturi:
        media = sum(temperaturi) / len(temperaturi)
        print(f"media temperaturilor este: {media}\n")
        print("temperaturile sunt:\n")
        for i in temperaturi:
            print(f"{i}\n")
    else:
        print("fisierul este gol :P")


"""
Problem 4: FizzBuzz with a Twist (Functions & Loops)
Create a function custom_fizzbuzz(n) that prints numbers from 1 to n.
For multiples of 3, print "Fizz",
for multiples of 5, print "Buzz",
for multiples of both 3 and 5, print "FizzBuzz".
For all other numbers, print the number itself.

Example: custom_fizzbuzz(5)
Output: 1
2
Fizz
4
Buzz
"""

def fizzbuzz(n):
    for i in range(1, n):
        if (i % 3 == 0) and (i % 5 == 0):
            print("FizzBuzz\n")
            return
        elif i % 3 == 0:
            print("Fizz\n")
            return
        elif i % 5 == 0:
            print("Buzz\n")
            return
        else:
            print(f"{i}\n")




"""
Problem 5.
Write a Python script that must recursively search within {start_directory} and all its subdirectories for all files (not directories)
that contain {search_name} in their name.
The value for the {search_name} and {start_directory} will be read from the keyboard.
The output should contain a list of full paths with all the files that matched the {search_name}.

Args:
    - search_name: A string representing the text to be searched for in filenames.
    - start_directory: The path to a directory where the search will begin.

Returns: The script will display the full paths to the found files, each on a new line.

Error Handling:
    - The script will display an error message and exit if essential inputs (search_name or start_directory)
      are empty or only contain whitespace when read from the keyboard.
    - An error message will be shown if the provided start_directory does not exist or is not a valid directory.

EXAMPLE:
    Structure model:
    test_search/
    ├── main_document_workshop.txt
    ├── workshop_archive.zip
    ├── images/
    │   ├── vacation_photo_workshop.jpg
    │   ├── screenshot.png
    │   └── another_document.txt
    └── project/
        ├── source_code/
        │   ├── main_module_workshop.py
        │   └── document_utils.py
        └── README_project_workshop.md

    If we search for the word "workshop" within the 'test_search/' directory,
    the script should output the following full paths:
        test_search/main_document_workshop.txt
        test_search/workshop_archive.zip
        test_search/images/vacation_photo_workshop.jpg
        test_search/project/source_code/main_module_workshop.py
        test_search/project/README_project_workshop.md
"""



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parola = input(f"dati parola\n")
    print(check_password_strength(parola))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
