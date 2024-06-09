from bs4 import BeautifulSoup
import re
from time import time
from utils.print_utils import draw_progress_bar

from utils.file import open_lines, write_line
from utils.time import AvgRemainingTime


def convert_symbols(string):
    return string.encode("latin-1").decode("utf-8")


def to_markup(character_tags, parent_tag="word"):
    jp_markup = ""
    for tag in character_tags:
        is_plain_string = isinstance(tag, str)
        if is_plain_string:
            jp_markup += convert_symbols(tag)
            continue

        symbol_markup = convert_symbols(''.join([t for t in tag.contents if isinstance(t, str)]))
        furigana_tag = tag.find("rt")

        if furigana_tag:
            furigana = convert_symbols(furigana_tag.text)
            symbol_markup = f'<kanji furigana="{furigana}">{symbol_markup}</kanji>'

        jp_markup += symbol_markup
    jp_markup = f'<{parent_tag}>{jp_markup}</{parent_tag}>'
    return jp_markup


if __name__ == "__main__":
    formatted_records = [x['character'] for x in open_lines("./out/kanji_dataset.txt")]

    kanji_dataset = open_lines("out/raw_pages_all.txt")

    avg_timer = AvgRemainingTime(total=len(kanji_dataset) - len(formatted_records))
    for record in kanji_dataset:
        if record['character'] in formatted_records:
            continue

        start_time = time()
        [examples, vocab, kanji] = [record["pages"]['examples'], record["pages"]['vocab'], record["pages"]['kanji']]

        page = BeautifulSoup(kanji, "html.parser")
        examples_section = BeautifulSoup(examples, "html.parser").find(attrs={'class': 'subsection-examples'})
        vocab_section = BeautifulSoup(vocab, "html.parser").find(attrs={'class': 'subsection-used-in'})

        try:
            kanji_section = BeautifulSoup(kanji, "html.parser").findAll(attrs={'class': 'subsection-composed-of-kanji'})[-1]
        except:
            kanji_section = None

        print(f'Processing {record['character']}')

        strings = ["Keyword", "Frequency", "Type", "Kanken", "Heisig"]

        values = [page.find(string=value) for value in strings]
        [keyword, frequency, kyouiku_grade, kanken_level, heisig] = [x.parent.nextSibling.text if x else None for x in
                                                                     values]

        if kyouiku_grade:
            kyouiku_grade_number = re.findall(r'\d+', kyouiku_grade)
            if len(kyouiku_grade_number):
                kyouiku_grade = int(re.findall(r'\d+', kyouiku_grade)[0])
            else:
                kyouiku_grade = None

        frequency = int(re.findall(r'\d+', frequency)[-1]) // 100

        readings_row = page.find(string="Readings").parent.parent
        uncommon_readings_row = readings_row.nextSibling

        percent_total = 0
        readings = []
        reading_rows = readings_row.findAll(lambda tag: tag.has_attr('style') and 'display: flex;' in tag['style'])
        for row in reading_rows:
            reading = row.find("a").text.encode("latin-1").decode("utf-8")
            percent = int(re.findall(r'\d+', row.find("div").text)[0])
            readings.append({'reading': reading, 'percent': percent})
            percent_total += percent

        if uncommon_readings_row:
            uncommon_readings = [x.text.encode("latin-1").decode("utf-8") for x in uncommon_readings_row.findAll("div")]
            reading_percent = (100 - percent_total) / len(uncommon_readings)
            readings += [{'reading': x, 'percent': reading_percent} for x in uncommon_readings]

        parts = []
        composed_of_text = page.find(string='Composed of')
        if composed_of_text:
            compounds = composed_of_text.parent.nextSibling.findAll(
                lambda tag: tag.name == "div" and not tag.has_attr('class') and
                            not tag.has_attr('style'))
            for item in compounds:
                symbol = item.find("a").text.encode("latin-1").decode("utf-8")
                meaning = item.find("div", attrs={'class': 'description'}).text
                parts.append({'symbol': symbol, 'meaning': meaning})

        mnemonic_html = page.find(attrs={'class': 'mnemonic'})

        # KANJI
        included_in_kanji = []
        if kanji_section:
            for kanji_record in kanji_section.findAll(attrs={'class': 'used-in'}):
                [character, meaning] = [kanji_record.find(attrs={'class': x}).text for x in ['spelling', 'description']]
                included_in_kanji.append({'character': character, 'meaning': meaning})

        # VOCAB
        vocab_rows = vocab_section.findAll(attrs={'class': 'used-in'})
        vocab = []
        for row in vocab_rows:
            character_tags = row.findAll("ruby")
            translations = [tr.strip() for tr in row.find(attrs={'class': 'en'}).text.split(';')]

            markup = to_markup(character_tags)
            vocab.append({'markup': markup, 'translations': translations})

        # EXAMPLES
        sentence_examples = []
        if examples_section:
            example_rows = examples_section.findAll(attrs={'class': 'used-in'})
            for example_tag in example_rows:
                has_audio = example_tag.previousSibling is not None
                audio_id = None
                if has_audio:
                    audio_id = example_tag.previousSibling.get('data-audio')

                translation = example_tag.find(attrs={'class': 'en'}).text

                character_tags = example_tag.find(attrs={'class': 'jp'}).children

                sentence_markup = to_markup(character_tags, "sentence")
                sentence_examples.append({'markup': sentence_markup, 'translation': translation, "audio_id": audio_id})

        parsed_record = {'character': record['character'], 'keyword': keyword,
                         'stats': {'frequency': frequency, 'kyouiku_grade': kyouiku_grade, 'kanken_level': kanken_level,
                                   'heisig': heisig}, 'readings': readings, 'composed_of': parts,
                         'mnemonic_html': str(mnemonic_html), 'included_in_kanji': included_in_kanji, 'vocab': vocab,
                         'examples': sentence_examples}
        write_line("./out/kanji_dataset.txt", parsed_record)
        time_elapsed = time() - start_time
        avg_timer.add_item(time_elapsed)

        draw_progress_bar(avg_timer.percent)
        print(avg_timer)
