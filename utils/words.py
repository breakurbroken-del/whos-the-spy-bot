import json
import random


WORDS_FILE = "data/words.json"


def get_random_words():

    with open(
        WORDS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    # Random category
    category = random.choice(
        list(data.keys())
    )

    words = data[category]

    # Minimum 2 words required
    if len(words) < 2:
        raise ValueError(
            f"Category '{category}' has less than 2 words."
        )

    # Pick 2 different words
    villager_word, spy_word = random.sample(
        words,
        2
    )

    return {
        "category": category,
        "villager_word": villager_word,
        "spy_word": spy_word
    }
