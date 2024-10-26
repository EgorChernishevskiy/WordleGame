import random

words_list = ["apple", "berry", "charm", "dance", "eagle"]  # Список слов для игры


def generate_target_word():
    return random.choice(words_list)
