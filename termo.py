# In this version we have word check (brazilian punctuation)

# Return random word from database
# check if guess in database otherwise ask other guess
# count frequency of chars of mistery word, we dont want to color more than occurrences of a char, ex: 'arara' and 'tábua' -> color 2 'a'
# transform guess in list, if we color string itself, length grows and we lost index
# use 2 loops for color cause we need to color first greens then yellows, 
#   ex: 'telha' and 'malha' -> you must color last 'a' in green, the other 'a' will not be colored
#   otherwise would color first 'a' in 'malha' in yellow and the last 'a' will not be colored

import string
import random
import collections 
import os
import time

GREEN = '\033[92m'
YELLOW = '\033[93m'
FAIL = '\033[91m'
BLUE = '\033[94m'
ENDC = '\033[0m'

def main():
    mistery_word_punctuation: str = returnWordFromDatabase()
    mistery_word = removePunctuation(mistery_word_punctuation)
    alphabet: dict[str, str] = {letter: letter for letter in string.ascii_uppercase}
    
    display: str = ''
    trys = 1
    while trys <= 6:
        displayData(alphabet, display)

        guess: str = input("Palpite: ").upper()
        guess = checkWordFromDatabase(guess)
        if not guess:
            print(f'{FAIL}Essa palavra não existe na lista{ENDC}')
            time.sleep(1)
            continue

        mistery_word_frequency: dict[str, int] = collections.Counter(mistery_word)
        guess_colored: list[str] = [char for char in guess]
        guess = removePunctuation(guess)

        #color greens
        color(guess,  guess_colored, mistery_word, mistery_word_frequency, alphabet, False)
        #color yellows
        color(guess,  guess_colored, mistery_word, mistery_word_frequency, alphabet, True)
                     
        if guess == mistery_word:
            display += f"{trys}ª tentativa: {GREEN}{mistery_word_punctuation}{ENDC}\n"
            displayData(alphabet, display)
            print(f'{GREEN}Você acertou!!!{ENDC} \U0001F60E')
            return
            
        display += f"{trys}ª tentativa: {''.join(guess_colored)}\n"
        trys += 1
    
    displayData(alphabet, display)
    print(f'{BLUE}Não foi dessa vez{ENDC} \U0001F614\nA palavra era {GREEN}{mistery_word_punctuation}{ENDC}')


# https://stackoverflow.com/questions/3540288/how-do-i-read-a-random-line-from-one-file
# https://youtu.be/A1iwzSew5QY
def returnWordFromDatabase() -> str:
    with open('./br-utf8.txt-5-letras.txt', 'r', encoding="utf8") as database:
        line = next(database)
        for num, aline in enumerate(database, 2):
            if random.randrange(num):
                continue
            line = aline
    return line.strip().upper()

def checkWordFromDatabase(guess) -> str:
    with open('./br-utf8.txt-5-letras.txt', 'r', encoding="utf8") as database:
        for word in database:
            word = word.strip().upper() 
            if len(word) != len(guess):
                continue
            
            if isAnyLetterDifferent(word, guess):
                continue
            else:
                return word
    return ''

def isAnyLetterDifferent(word, guess) -> bool:
    for data_letter, guess_letter in zip(word, guess):
        if data_letter == guess_letter:
            pass
        elif guess_letter == 'A'and data_letter in ('Á', 'À', 'Â', 'Ã'):
            pass
        elif guess_letter == 'E' and data_letter in ('É', 'Ê'):
            pass
        elif guess_letter == 'I' and data_letter == 'Í':
            pass
        elif guess_letter == 'O' and data_letter in ('Ó', 'Ô', 'Õ'):
            pass
        elif guess_letter == 'U' and data_letter == 'Ú':
            pass
        elif guess_letter == 'C' and data_letter == 'Ç':
            pass
        else:
            return True
    return False

def color(guess: str, painted_word: list[str], mistery_word: str, letters_frequency: dict[str,int], alphabet: dict[str,str], is_green_colored: bool) -> None:
    for i, char in enumerate(guess):
        if char not in letters_frequency:
            alphabet[char] = char.join((FAIL, ENDC))
        else:
            if letters_frequency.get(char, 0) > 0:
                if mistery_word[i] == guess[i] and is_green_colored == False:
                    painted_word[i] = painted_word[i].join((GREEN, ENDC))
                    alphabet[char] = char.join((GREEN, ENDC)) 
                    letters_frequency[char] -= 1
                
                if is_green_colored and GREEN not in painted_word[i]:
                    painted_word[i] = painted_word[i].join((YELLOW, ENDC))
                    letters_frequency[char] -= 1
                    
                    if GREEN not in alphabet[char]:
                        alphabet[char] = char.join((YELLOW, ENDC))

def removePunctuation(word) -> str:
    for char in word:
        if char in ('Á', 'À', 'Â', 'Ã'):
            new = 'A'
        elif char in ('É', 'Ê'):
            new = 'E'
        elif char == 'Í':
            new = 'I'
        elif char in ('Ó', 'Ô', 'Õ'):
            new = 'O'
        elif char == 'Ú':
            new = 'U'
        elif char == 'Ç':
            new = 'C'
        else:
            continue
        word = word.replace(char, new)
    return word

def displayData(alphabet: dict[str, str], data: str) -> None:
    os.system('cls') #clear terminal
    print('+----------------------------------------------------+')
    print('|              Termo  |  Guilherme Possas            |')           
    print('+----------------------------------------------------+')
    print('|', end='')
    [print(letter, end=' ') for letter in alphabet.values()]
    print('|')
    print('+----------------------------------------------------+')
    print(data if data else '', end='')

main()