import os

from utils.file import open_lines
from constants import ROOT_DIR


class KanshudoRecord:
    def __init__(self, record):
        self.kanji = record['kanji']["character"]
        self.meaning = record['kanji']["meaning"]

        self.strokes = record['main_stats']['strokes']
        self.frequency = record['main_stats']["frequency"]
        self.jlpt_level = record['main_stats']["jlpt"]
        self.usefulness = record['main_stats']["usefulness"]
        self.grade = record['main_stats']["grade"]

        self.words = record['words']

    def __str__(self):
        return f'Kanshudo: {self.kanji} means {self.meaning}'


class KanshudoCollection:
    def __init__(self):
        self.collection = open_lines(os.path.join(ROOT_DIR, "./kanshudo/out/raw_formatted.txt"))

    def get_record_by_index(self, index):
        if index <= len(self.collection) - 1:
            return KanshudoRecord(self.collection[index])
        else:
            raise IndexError()

    def get_record_by_kanji(self, kanji_character):
        filtered = list(filter(lambda x: kanji_character == x["kanji"]["character"], self.collection))
        if len(filtered) == 1:
            return KanshudoRecord(filtered[0])
        else:
            raise KeyError(kanji_character)

    def group_by_usefulness(self):
        arr_dict = {}
        for record in self.collection:
            index = record["main_stats"]["usefulness"] - 1
            if arr_dict.get(index) is None:
                arr_dict[index] = []
            arr_dict[index].append(record)
        return [arr_dict.get(i) for i in range(max(arr_dict) + 1)]

    def group_by_jlpt(self):
        jlpt_levels = {}
        for record in self.collection:
            level = record["main_stats"]["jlpt"]
            if jlpt_levels.get(level) is None:
                jlpt_levels[level] = []
            jlpt_levels[level].append(KanshudoRecord(record))
        for key, array in jlpt_levels.items():
            jlpt_levels[key] = sorted(array, key=lambda rec: rec.usefulness)
        return jlpt_levels
