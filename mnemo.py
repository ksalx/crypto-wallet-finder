import itertools
import random


def generate_seeds():
    with open('bip39-2048.txt', 'r') as f:
        lines = f.readlines()
        words = []

        while True:
            for line in lines:
                words.append(line.strip())
            random.shuffle(words)
            temp_seed = random.choices(words, k=11)
            result = []
            for word in words:
                if word in temp_seed:
                    continue
                else:
                    result.append(temp_seed + [word])

            for seed in result:
                yield seed


def generate_seeds_nb():
    with open('bip39-2048.txt', 'r') as f:
        lines = f.readlines()
        words = []
        for line in lines:
            words.append(line.strip())
        random.shuffle(words)
        while True:
            n = random.choices(words, k=12)
            yield n


def generate_seeds_nt():
    with open('bip39-2048.txt', 'r') as f:
        lines = f.readlines()
        words = []
        for line in lines:
            words.append(line.strip())
        temp_list = random.choices(words, k=12)
        res = itertools.permutations(temp_list, r=12)
        for i in res:
            yield list(i)
