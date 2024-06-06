import os

from utils.file import open_lines, write_line
from constants import ROOT_DIR
from kanshudo.collection import KanshudoCollection


class WanikaniLevel:
    kanshudo_col = KanshudoCollection()

    def __init__(self, record, level):
        self.level = level
        self.radicals = record['radicals'] if record.get('radicals') else None
        self.kanji = filter(lambda item: item['character'] != '々', record['kanji'])
        self.words = record['words']

        self.jlpt_levels = list({self.kanshudo_col.get_record_by_kanji(kanji['character']).jlpt_level for kanji in
                                 self.kanji})

    def __str__(self):
        return f"Wanikani Level #{self.level}: {' '.join([x['character'] for x in self.kanji])}"


class WanikaniKanjiRecord:
    def __init__(self, record):
        self.kanji = record['character']
        self.radicals = record['radicals']
        self.onyomi = record['readings']['onyomi'] if record['readings'].get('onyomi') else None
        self.kunyomi = record['readings']['kunyomi'] if record['readings'].get('kunyomi') else None
        self.mnemonic = record['readings']['mnemonic']['text']
        self.mnemonic_hint = record['readings']['mnemonic']['hint']
        self.words = record['words']

    def __str__(self):
        return f"Wanikani record {self.kanji}"


class WanikaniCollection:
    def __init__(self):
        self.kanji_collection = [WanikaniKanjiRecord(item) for item in
                                 open_lines(os.path.join(ROOT_DIR, "./wanikani/out/kanji_updated.txt"))]
        levels = open_lines(os.path.join(ROOT_DIR, "./wanikani/out/levels.txt"))[0]
        self.level_collection = [WanikaniLevel(levels[index], index + 1) for index in range(len(levels))]

    def get_kanji(self, character):
        filtered = list(filter(lambda item: item.kanji == character, self.kanji_collection))
        if len(filtered) == 1:
            return filtered[0]
        else:
            raise KeyError(character)


if __name__ == "__main__":
    pass
    # n5_radicals = [rec.radicals for rec in n5_wanikani_records]
    # print(n5_radicals)
    # radicals_set = set(radical for radical in n5_radicals)
    #
    # print(n5_radicals)
