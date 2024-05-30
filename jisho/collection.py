import os

from utils.file import open_lines
from constants import ROOT_DIR


class JishoRecord:
    def __init__(self, record):
        self.kanji = record['kanji']
        self.meanings = record['main_meanings']

        self.on_readings = record['readings']['on']
        self.kun_readings = record['readings']['kun']

        self.grade = record['stats']['grade']
        self.jlpt_level = record['stats']['jlpt']
        self.frequency = record['stats']['frequency']

        self.compounds = record['compounds']

    def __str__(self):
        return f'Jisho: {self.kanji} means {self.meanings}'


class JishoCollection:
    def __init__(self):
        self.collection = open_lines(os.path.join(ROOT_DIR, "./jisho/out/filled_data.txt"))

    def get_record_by_index(self, index):
        if index <= len(self.collection) - 1:
            return JishoRecord(self.collection[index])
        else:
            raise IndexError()

    def get_record_by_kanji(self, kanji_character):
        filtered = list(filter(lambda x: kanji_character == x["kanji"], self.collection))
        if len(filtered) == 1:
            return JishoRecord(filtered[0])
        else:
            raise KeyError(kanji_character)

    def group_by_jlpt(self):
        jlpt_levels = {}
        for record in self.collection:
            level = record["stats"]["jlpt"]
            if jlpt_levels.get(level) is None:
                jlpt_levels[level] = []
            jlpt_levels[level].append(JishoRecord(record))
        for key, array in jlpt_levels.items():
            jlpt_levels[key] = sorted(array,
                                      key=lambda rec: rec.frequency if rec.frequency is not None else float('inf'))
        return jlpt_levels

    def order_by_frequency(self):
        return sorted(self.collection,
                      key=lambda rec: rec["stats"]["frequency"] if rec["stats"]["frequency"] is not None else float(
                          'inf'))
