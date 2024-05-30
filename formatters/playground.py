from deep_translator import GoogleTranslator, MyMemoryTranslator

from utils.file import open_lines, write_line
from utils.print_utils import draw_progress_bar
from jisho.collection import JishoCollection
from kanshudo.collection import KanshudoCollection
from synonym.generator import get_synonym
from yarxi.parser import get_yarxi_translation

if __name__ == "__main__":
    jisho_col = JishoCollection()
    kanshudo_col = KanshudoCollection()

    mnemonic_inputs = open_lines("./kanji_mnemonic_gen.json")

    finished_characters = [x['character'] for x in open_lines("./out/mnemonic_dataset.txt")]

    for index in range(len(mnemonic_inputs)):
        record = mnemonic_inputs[index]
        if record['character'] in finished_characters:
            continue

        print(record['character'])
        meanings_str = ", ".join(jisho_col.get_record_by_kanji(record['character']).meanings)
        translated = GoogleTranslator(source='english', target='russian').translate(meanings_str)

        translated_meanings = [word.strip().lower() for word in translated.split(",")]
        added_meanings = set([z.lower() for z in get_yarxi_translation(record['character'])] + translated_meanings)

        radicals_ru = list(
            set([x.lower() for x in get_synonym(word)] + [word.lower()]) for word in record['radicals_ru'])

        result = {'meanings_ru': list(added_meanings), "radicals_ru": [list(x) for x in radicals_ru],
                  'character': record['character']}

        draw_progress_bar(index / len(mnemonic_inputs))
        write_line("./out/mnemonic_dataset.txt", result)