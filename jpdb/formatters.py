from bs4 import BeautifulSoup
import re
from time import time
from utils.print_utils import draw_progress_bar

from utils.file import open_lines, write_line, open_json
from utils.time import AvgRemainingTime

word_page_sample = {
    "page": "<body data-instant-allow-query-string=\"\"><div class=\"nav\"><h1 class=\"nav-logo\"><a href=\"/\">jpdb</a> <span style=\"font-size: 50%\">beta</span></h1><a class=\"nav-item\" href=\"/login\">Login or Sign up</a></div><div class=\"container bugfix\"><div class=\"result vocabulary\"><div class=\"hbox gap\"><div class=\"subsection-spelling with-furigana\"><div class=\"primary-spelling\"><div class=\"spelling\"><div><ruby class=\"v\">ã½ã¼ã<rt></rt>æ°´<rt>ãã</rt></ruby></div></div></div></div><div class=\"subsection-meanings\"><h6 class=\"subsection-label\">Meanings</h6><div class=\"subsection\"><div class=\"part-of-speech\"><div>Noun</div></div><div class=\"description\">1.  soda water</div></div></div></div></div><table class=\"cross-table label-right-align data-right-align\" style=\"margin-top: 1.5rem\"><tr><th></th><th>Used in</th><th>Used in %</th></tr><tr><td>Anime</td><td>0</td><td style=\"opacity: 0.75\">(0%)</td></tr><tr><td>Live action</td><td>0</td><td style=\"opacity: 0.75\">(0%)</td></tr><tr><td>Visual novels</td><td>3</td><td style=\"opacity: 0.75\">(0%)</td></tr><tr><td>Novels</td><td>2</td><td style=\"opacity: 0.75\">(0%)</td></tr><tr><td>Non-fiction</td><td>0</td><td style=\"opacity: 0.75\">(0%)</td></tr><tr><td>Web novels</td><td>0</td><td style=\"opacity: 0.75\">(0%)</td></tr><tr><td>Aozora Bunko</td><td>0</td><td style=\"opacity: 0.75\">(0%)</td></tr></table><h4>Used in</h4><fieldset><legend>Show only</legend><div class=\"sorting-header\"><a href=\"/vocabulary/1965530/ã½ã¼ãæ°´/used-in?show_only=anime\">Anime</a><a href=\"/vocabulary/1965530/ã½ã¼ãæ°´/used-in?show_only=live_action\">Live action</a><a href=\"/vocabulary/1965530/ã½ã¼ãæ°´/used-in?show_only=visual_novel\">Visual novels</a><a href=\"/vocabulary/1965530/ã½ã¼ãæ°´/used-in?show_only=novel\">Novels</a><a href=\"/vocabulary/1965530/ã½ã¼ãæ°´/used-in?show_only=non_fiction\">Books (non-fiction)</a><a href=\"/vocabulary/1965530/ã½ã¼ãæ°´/used-in?show_only=web_novel\">Web novels</a><a href=\"/vocabulary/1965530/ã½ã¼ãæ°´/used-in?show_only=aozora\">Aozora Bunko</a></div></fieldset><p style=\"opacity: 0.75; text-align: right;\">Showing 1..5 from 5 entries</p><div style=\"display: flex; flex-wrap: wrap;\"><div style=\"display: flex; flex-direction: column; margin-right: 2rem; margin-bottom: 0.5rem;\"><div style=\"margin-bottom: 0.75rem; min-width: 11rem; display: flex; justify-content: flex-end;\"><img alt=\"Cover of Dorakuriusu\" loading=\"lazy\" src=\"/static/ee3622878601.jpg\" style=\"max-height: 17rem; max-width: 11rem;\"/></div></div><div style=\"margin-bottom: 3rem; margin-right: 1.5rem; display: flex; flex-direction: column; align-items: flex-start;\"><div style=\"opacity: 0.5\">Visual novel</div><h5 style=\"max-width: 30rem;\">Dorakuriusu</h5><div style=\"margin-left: 0.5rem; display: flex; flex-direction: column; flex-grow: 1; align-items: flex-start;\"><table class=\"cross-table data-right-align\"><tr><th>Used times</th><td>2</td></tr></table><div style=\"flex-grow: 1; min-height: 1rem;\"></div><div style=\"margin-top: 0.5rem;\"><a class=\"outline\" href=\"/visual-novel/5396/dorakuriusu\">See in database...</a></div></div></div></div><div style=\"display: flex; flex-wrap: wrap;\"><div style=\"display: flex; flex-direction: column; margin-right: 2rem; margin-bottom: 0.5rem;\"><div style=\"margin-bottom: 0.75rem; min-width: 11rem; display: flex; justify-content: flex-end;\"><img alt=\"Cover of Fairytale Requiem\" loading=\"lazy\" src=\"/static/e6d2df496d4d.jpg\" style=\"max-height: 17rem; max-width: 11rem;\"/></div></div><div style=\"margin-bottom: 3rem; margin-right: 1.5rem; display: flex; flex-direction: column; align-items: flex-start;\"><div style=\"opacity: 0.5\">Visual novel</div><h5 style=\"max-width: 30rem;\">Fairytale Requiem</h5><div style=\"margin-left: 0.5rem; display: flex; flex-direction: column; flex-grow: 1; align-items: flex-start;\"><table class=\"cross-table data-right-align\"><tr><th>Used times</th><td>1</td></tr></table><div style=\"flex-grow: 1; min-height: 1rem;\"></div><div style=\"margin-top: 0.5rem;\"><a class=\"outline\" href=\"/visual-novel/3997/fairytale-requiem\">See in database...</a></div></div></div></div><div style=\"display: flex; flex-wrap: wrap;\"><div style=\"display: flex; flex-direction: column; margin-right: 2rem; margin-bottom: 0.5rem;\"><div style=\"margin-bottom: 0.75rem; min-width: 11rem; display: flex; justify-content: flex-end;\"><img alt=\"Cover of Shirokuro Nekuro\" loading=\"lazy\" src=\"/static/121f682fe3f6.jpg\" style=\"max-height: 17rem; max-width: 11rem;\"/></div></div><div style=\"margin-bottom: 3rem; margin-right: 1.5rem; display: flex; flex-direction: column; align-items: flex-start;\"><div style=\"opacity: 0.5\">Novel</div><h5 style=\"max-width: 30rem;\">Shirokuro Nekuro</h5><div style=\"margin-left: 0.5rem; display: flex; flex-direction: column; flex-grow: 1; align-items: flex-start;\"><table class=\"cross-table data-right-align\"><tr><th>Used times</th><td>1</td></tr></table><div style=\"flex-grow: 1; min-height: 1rem;\"></div><div style=\"margin-top: 0.5rem;\"><a class=\"outline\" href=\"/novel/6190/shirokuro-nekuro\">See in database...</a></div></div></div></div><div style=\"display: flex; flex-wrap: wrap;\"><div style=\"display: flex; flex-direction: column; margin-right: 2rem; margin-bottom: 0.5rem;\"><div style=\"margin-bottom: 0.75rem; min-width: 11rem; display: flex; justify-content: flex-end;\"><img alt=\"Cover of Tsubasa wo Kudasai\" loading=\"lazy\" src=\"/static/9f67bf807ffc.jpg\" style=\"max-height: 17rem; max-width: 11rem;\"/></div></div><div style=\"margin-bottom: 3rem; margin-right: 1.5rem; display: flex; flex-direction: column; align-items: flex-start;\"><div style=\"opacity: 0.5\">Novel</div><h5 style=\"max-width: 30rem;\">Tsubasa wo Kudasai</h5><div style=\"margin-left: 0.5rem; display: flex; flex-direction: column; flex-grow: 1; align-items: flex-start;\"><table class=\"cross-table data-right-align\"><tr><th>Used times</th><td>1</td></tr></table><div style=\"flex-grow: 1; min-height: 1rem;\"></div><div style=\"margin-top: 0.5rem;\"><a class=\"outline\" href=\"/novel/7734/tsubasa-wo-kudasai\">See in database...</a></div></div></div></div><div style=\"display: flex; flex-wrap: wrap;\"><div style=\"display: flex; flex-direction: column; margin-right: 2rem; margin-bottom: 0.5rem;\"><div style=\"margin-bottom: 0.75rem; min-width: 11rem; display: flex; justify-content: flex-end;\"><img alt=\"Cover of Ai Kiss 2\" loading=\"lazy\" src=\"/static/5ae27700dbda.jpg\" style=\"max-height: 17rem; max-width: 11rem;\"/></div></div><div style=\"margin-bottom: 3rem; margin-right: 1.5rem; display: flex; flex-direction: column; align-items: flex-start;\"><div style=\"opacity: 0.5\">Visual novel</div><h5 style=\"max-width: 30rem;\">Ai Kiss 2</h5><div style=\"margin-left: 0.5rem; display: flex; flex-direction: column; flex-grow: 1; align-items: flex-start;\"><table class=\"cross-table data-right-align\"><tr><th>Used times</th><td>1</td></tr></table><div style=\"flex-grow: 1; min-height: 1rem;\"></div><div style=\"margin-top: 0.5rem;\"><a class=\"outline\" href=\"/visual-novel/15700/ai-kiss-2\">See in database...</a></div></div></div></div><div style=\"padding-top: 0.75rem;\"></div></div><hr class=\"bottom\"/><footer class=\"footer\"><a href=\"/about\">About</a><a href=\"/faq\">FAQ</a><a href=\"/contact-us\">Contact us</a><a href=\"/privacy-policy\">Privacy policy</a><a href=\"/terms-of-use\">Terms of use</a><a href=\"/changelog\">Changelog</a></footer><script defer=\"\" src=\"/static/ae433897feb1.js\" type=\"module\"></script></body>",
    "word_id": 1965530}


def convert_symbols(string):
    return string.encode("latin-1").decode("utf-8")


def to_snake_case(string):
    return string.replace("-", " ").lower().replace(" ", "_")


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


def format_kanji_pages():
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
            kanji_section = \
                BeautifulSoup(kanji, "html.parser").findAll(attrs={'class': 'subsection-composed-of-kanji'})[-1]
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


def get_word_str(page):
    [word_markup, word_str] = ['', '']
    word_tag = page.find("ruby")
    if word_tag is None:
        print(page)
    word_tag_children = list(word_tag.children)
    for index in range(0, len(word_tag_children), 2):
        character = word_tag_children[index]
        furigana = word_tag_children[index + 1].text

        if furigana:
            word_markup += f'<kanji furigana="{furigana}">{character}</kanji>'
        else:
            word_markup += character

        word_str += character
    return word_str


def get_media_records(page):
    media = []
    media_tags = page.findAll('div', style="display: flex; flex-wrap: wrap;")
    for tag in media_tags:
        genre = tag.find("div", style="opacity: 0.5").text.lower()
        title = tag.find('h5').text
        use_count = int(tag.find('td').text)
        media_id = int(tag.find('a').get('href').split('/')[2])
        media.append({'genre': genre, 'title': title, 'use_count': use_count, 'media_id': media_id})
    return media


def format_word_record(record):
    page = BeautifulSoup(record["page"], "html.parser")

    word_id = record["word_id"]

    # WORD
    [word_markup, word_str] = ['', '']
    word_tag = page.find("ruby")
    word_tag_children = list(word_tag.children)
    for index in range(0, len(word_tag_children), 2):
        character = word_tag_children[index]
        furigana = word_tag_children[index + 1].text

        if furigana:
            word_markup += f'<kanji furigana="{convert_symbols(furigana)}">{convert_symbols(character)}</kanji>'
        else:
            word_markup += convert_symbols(character)

        word_str += convert_symbols(character)

    meanings_container = page.find(string="Meanings").parent.nextSibling

    # PARTS OF SPEECH AND MEANINGS
    parts_of_speech_tag = meanings_container.find(attrs={'class': 'part-of-speech'})
    parts_of_speech = re.split(r',(?![^\[\]()]*[])])', parts_of_speech_tag.text) if parts_of_speech_tag else None

    meanings = []
    meaning_tags = meanings_container.findAll(attrs={'class': 'description'})
    for meaning in meaning_tags:
        meaning_group = [x.strip() for x in meaning.text[4:].split(";")]
        meanings.append(meaning_group)

    # STATS
    stat_labels = ['Anime', 'Live action', 'Visual novels', 'Novels', 'Non-fiction', 'Web novels', 'Aozora Bunko']
    stat_rows = [page.find(string=x).parent.parent for x in stat_labels]
    stats = {}
    for row in stat_rows:
        [label, count, percent] = [x.text for x in list(row.children)]
        key = to_snake_case(label)
        stats[key] = (int(count), int(percent[1:-2]))

    # MEDIA BREAKDOWN
    media = []
    media_tags = page.findAll('div', style="display: flex; flex-wrap: wrap;")
    for tag in media_tags:
        genre = tag.find("div", style="opacity: 0.5").text.lower()
        title = tag.find('h5').text
        use_count = int(tag.find('td').text)
        media_id = int(tag.find('a').get('href').split('/')[2])
        media.append({'genre': genre, 'title': title, 'use_count': use_count, 'media_id': media_id})

    return {"word_id": word_id, "word_markup": word_markup, "word_str": word_str, "parts_of_speech": parts_of_speech,
            "meanings": meanings, "stats": stats, "media": media}


if __name__ == "__main__":
    pass
    # json_data = open_json("./out/formatted_media_records.txt")
    #
    # for [media_id, record] in json_data.items():
    #     flat_record = {'id': media_id, **record}
    #     write_line('./out/flat_media_records.txt', flat_record)
    #
    # print("Finished writing!")

    # formatted_records = [len(x['words']) for x in open_json('./out/formatted_media_records.txt').values()]
    # print(sum(formatted_records))

    # start_time = time()
    # media_words = open_lines("./out/extra_media_record.txt")
    # open_time = time()
    # print(f"File opened in {open_time - start_time}")
    #
    # formatted_media = {}
    # for media_word in media_words:
    #     word_details = {'word_id': media_word['word_id'], 'word_str': media_word['word_str'],
    #                     'use_count': media_word['use_count']}
    #
    #     if formatted_media.get(media_word['media_id']) is None:
    #         formatted_media[media_word['media_id']] = {'genre': media_word['genre'], 'title': media_word['title'],
    #                                                    'words': [word_details]}
    #     else:
    #         formatted_media[media_word['media_id']]['words'].append(word_details)
    #
    # processing_time = time()
    # print(f'Processed in {processing_time - open_time}')
    # write_line("./out/formatted_media_records.txt", formatted_media)
    # print(f'Finished writing in {time() - processing_time}')

    # finished_words_ids = [x['word_id'] for x in open_lines("./out/words_formatted.txt")]
    #
    # words_src = open_lines("./out/words_all.txt")
    #
    # avg_timer = AvgRemainingTime(total=len(words_src) - len(finished_words_ids))
    # for record in words_src:
    #     if record['word_id'] in finished_words_ids:
    #         continue
    #
    #     print(f'Processing {record['word_id']}')
    #     start_time = time()
    #     formatted = format_word_record(record)
    #     write_line("./out/words_formatted.txt", formatted)
    #
    #     avg_timer.add_item(time() - start_time)
    #     draw_progress_bar(avg_timer.percent)
    #     print(avg_timer)

    # format_kanji_pages()
    # print(format_word_record(word_page_sample))
