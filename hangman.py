# Problem Set 2, hangman.py
# Name: Pobiedimska Sonya
# Collaborators: none
# Time spent: started on 07/12/19 at 11.30, ended up on 07/12/19 at 14.30


# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def validate(prompt_input, prompt_error_length, prompt_error_not_letter, prompt_error_not_in_list, letters_guessed,
             warnings_remaining):
    must_continue = True
    assumption = input(prompt_input).replace(' ', '')
    while must_continue:
        if assumption == '*':
            break
        if not assumption.isalpha():
            warnings_remaining -= 1
            print(prompt_error_not_letter, 'You have ', str(warnings_remaining), ' warnings left:')
        elif len(assumption) is not 1:
            warnings_remaining -= 1
            print(prompt_error_length, 'You have ', str(warnings_remaining), ' warnings left:')
        elif assumption in letters_guessed:
            warnings_remaining -= 1
            print(prompt_error_not_in_list, 'You have ', str(warnings_remaining), ' warnings left:')
        else:
            break
        if warnings_remaining <= 0:
            assumption = ''
            break
        assumption = input(prompt_input)
    return assumption


def is_word_guessed(secret_word, letters_guessed):
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    remade_word = []
    for letter in secret_word:
        if letter not in letters_guessed:
            new_char = '_ '
        else:
            new_char = letter
        remade_word.append(new_char)
    return ''.join(remade_word)


def get_available_letters(letters_guessed):
    alphabet = string.ascii_lowercase
    avaliable_letters = []
    for letter in alphabet:
        if letter not in letters_guessed:
            avaliable_letters.append(letter)
    return ''.join(avaliable_letters)


def attempts_left(guess_amount, available_letters):
    print('-------------')
    print('You have ', str(guess_amount), ' guesses left.')
    print('Available letters: ', available_letters)

def hangman(secret_word):
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3
    vowels = ['a', 'o', 'u', 'e', 'i']

    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is ', len(secret_word), ' letters long.')

    while guesses_remaining > 0:
        available_letters = get_available_letters(letters_guessed)
        attempts_left(guesses_remaining, available_letters)
        assumption = validate("Please guess a letter: ", "Oops! That does not look like a single letter. ",
                              "Oops! That is not a valid letter. ", "Oops! You\'ve already guessed that letter. ",
                              letters_guessed, warnings_remaining)
        while assumption in letters_guessed and warnings_remaining > 0:
            warnings_remaining -= 1
            print('Oops! You\'ve already guessed that letter. You have ', str(warnings_remaining), ' warnings left:',
                  get_available_letters(letters_guessed))
            assumption = input("Please guess a letter: ")
        if assumption == '':
            break
        else:
            letters_guessed.append(assumption)
        if assumption in secret_word:
            print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
                break
        elif assumption == "*":
            print('This is not a version with hints :) ')
        else:
            print('Oops! That letter is not in my word: ', get_guessed_word(secret_word, letters_guessed))
            if assumption in vowels:
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
    print('.-.-.-.-.-.-.-.')
    if is_word_guessed(secret_word, letters_guessed):
        print('Congratulations, you won!\nYour total score for this game is: ' + str(
            guesses_remaining * len(secret_word)))
    else:
        print('Sorry, you ran out of guesses. The word was: ', secret_word, '')


# -----------------------------------


def match_with_gaps(my_word, other_word):
    corrected_word = my_word.replace(' ', '')
    if len(corrected_word) is not len(other_word):
        return False
    for i in range(len(corrected_word)):
        if (corrected_word[i] != '_' and corrected_word[i] != other_word[i]) or (other_word[i] in corrected_word and corrected_word[i] == '_'):
            return False
    return True


def show_possible_matches(my_word):
    string = ''
    for word in wordlist:
        if match_with_gaps(my_word, word):
            string += word +' '
    if string == '':
        string += 'No matches found'
    print(string)


def hangman_with_hints(secret_word):
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3
    vowels = ['a', 'o', 'u', 'e', 'i']

    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is ', len(secret_word), ' letters long.')

    while guesses_remaining > 0:
        available_letters = get_available_letters(letters_guessed)
        attempts_left(guesses_remaining, available_letters)
        assumption = validate("Please guess a letter: ", "Oops! That does not look like a single letter. ",
                              "Oops! That is not a valid letter. ", "Oops! You\'ve already guessed that letter. ",
                              letters_guessed, warnings_remaining)
        while assumption in letters_guessed and warnings_remaining > 0:
            warnings_remaining -= 1
            print('Oops! You\'ve already guessed that letter. You have ', str(warnings_remaining), ' warnings left:',
                  get_available_letters(letters_guessed))
            assumption = input("Please guess a letter: ")

        if assumption == '':
            break
        letters_guessed.append(assumption)
        if assumption in secret_word:
            print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
                break
        # addition to a hangman
        elif assumption == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        # end of addition
        else:
            print('Oops! That letter is not in my word: ', get_guessed_word(secret_word, letters_guessed))
            if assumption in vowels:
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
    print('.-.-.-.-.-.-.-.')
    if is_word_guessed(secret_word, letters_guessed):
        print('Congratulations, you won!\nYour total score for this game is: ' + str(
            guesses_remaining * len(secret_word)))
    else:
        print('Sorry, you ran out of guesses. The word was: ', secret_word, '')


if __name__ == "__main__":
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
