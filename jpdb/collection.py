import os

from utils.file import open_lines
from constants import ROOT_DIR


class JpDBKanjiRecord:
    def __init__(self, record):
        self.kanji = record['character']
        self.keyword = record['keyword']
        self.stats = record['stats']
        self.readings = record['readings']
        self.composed_of = record['composed_of']
        self.mnemonic_html = record['mnemonic_html']
        self.included_in_kanji = record['included_in_kanji']
        self.vocab = record['vocab']
        self.examples = record['examples']

    def __str__(self):
        return (f'JpDBKanjiRecord for character "{self.kanji}". Included in {len(self.included_in_kanji or [])} kanji,'
                f' {len(self.vocab or [])} vocab words and {len(self.examples or [])} example sentences')


class JpDBCollection:
    def __init__(self):
        self.collection = [JpDBKanjiRecord(x) for x in
                           open_lines(os.path.join(ROOT_DIR, "./jpdb/out/kanji_dataset.txt"))]

    def get_by_index(self, index):
        if index <= len(self.collection) - 1:
            return self.collection[index]
        else:
            raise IndexError(f" '{index}' is out of range (0, {len(self.collection)})")

    def get_by_kanji(self, kanji_character):
        filtered = list(filter(lambda record: kanji_character == record.kanji, self.collection))
        if len(filtered) == 1:
            return filtered[0]
        else:
            raise KeyError(kanji_character)


if __name__ == "__main__":
    col = JpDBCollection()
    print(col.get_by_index(654))
