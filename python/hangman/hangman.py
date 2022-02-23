import random
import os
from colorama import Fore, Style, Back, init
import codecs

def add_answer(file: str, word):
    with codecs.open(file, "a+", encoding='utf-8',errors="ignore") as f:
        f.seek(0)
        words = f.read().split(",")
        if word not in words:  # Предотвращение появления дубликатов
            f.seek(0, 2)
            f.write(word + ',')


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command=command)


def read_answers(file: str):
    with codecs.open(file, "r", encoding='utf-8',errors="ignore") as f:
        words = f.read().split(",")
        print("На этом устройстве были отгаданы такие слова:")
        for word in words:
            print(word)


def get_word(file: str):
    with codecs.open(file, "r", encoding='utf-8',errors="ignore") as f:
        arr = f.read().splitlines()
        newmarr = []
        for string in arr:  # Убираю символы \n из файла
            newmarr += list(filter(None, string.split(",")))
        return random.choice(newmarr)


def open_chars(char: str, current: str, answer: str):
    for i in range(len(answer)):
        if answer[i] == char:
            current[i] = char


def game_loop(word: str):
    messages = {5: "всё в порядке", 4: "попытка - не пытка", 3: "стоит задуматься", 2: "что-то идёт не по плану",
                1: "последний шанс"}
    remainlives = 5
    answer = list(word.lower()) #слово
    word_in_progress = [" _ " for i in range(len(word))] #"зашифрованное" слово
    wrongletters=[]
    while answer != word_in_progress and remainlives > 0:
        clear_console()
        print(f"\nОсталось попыток: {remainlives} , {messages[remainlives]}")
        print("Текущее состояние ответа -", end="")
        for char in word_in_progress:
            print(char, end="")
        print("\nНеугаданные буквы: ", end="")
        for word in wrongletters:
            print(word+",", end="")
        print("\nВведите букву(в нижнем регистре):", end="")
        user_char = input().lower()
        if user_char in answer:
            open_chars(user_char, word_in_progress, answer)
            print(Fore.LIGHTYELLOW_EX + f"Открываю букву {user_char}")
        else:
            print(Fore.RED + "Упс, такой буквы в слове нет")
            remainlives -= 1
            if user_char not in wrongletters:
                wrongletters.append(user_char)
    if answer == word_in_progress:
        print(f'Ура!Ты победил, заношу слово {"".join(answer)} в отгаданные слова!')
        add_answer("answers.txt", "".join(answer))
    else:
        print(f"Проигрыш!Не надо печалиться - вся жизнь впереди. Было загадано слово {''.join(answer)}")


def get_choice():
    print(
        Fore.LIGHTGREEN_EX + "\nДобро пожаловать в Виселицу!\n1.Начать игру со случайным словом!\n2.Отгаданные слова\n3.Выход")
    while True:
        try:
            choice = int(input())
            if choice < 1 or choice > 3:
                print(Fore.RED + "Введите число от 1 до 3 включительно")
                continue
            else:
                break
        except ValueError:
            print(Fore.RED + "Введите корректное число")
    return choice


def main_loop():
    while True:
        choice = get_choice()
        if choice == 1:  # Не выделил в отдельную функцию чтобы делать break
            clear_console()
            game_loop(get_word("words.txt"))
        elif choice == 2:
            try:
                read_answers("answers.txt")
            except FileNotFoundError:
                print('\033[31m' + "На этом устройстве еще не отгадано ни одного слова!")
        elif choice == 3:
            break
        else:
            raise ValueError


main_loop()
