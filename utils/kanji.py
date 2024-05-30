from utils.file import open_json


def get_kanji_levels():
    return open_json("../levels.json")


if __name__ == "__main__":
    print([char['character'] for char in get_kanji_levels()[1]['kanji']])