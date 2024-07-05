from bs4 import BeautifulSoup

from utils.file import open_lines, open_json, write_line, rewrite_file


def to_markup(character_tags, parent_tag="word"):
    jp_markup = ""
    for tag in character_tags:
        is_plain_string = isinstance(tag, str)
        if is_plain_string:
            jp_markup += tag
            continue

        symbol_markup = ''.join([t for t in tag.contents if isinstance(t, str)])
        furigana_tag = tag.find("rt")

        if furigana_tag:
            furigana = furigana_tag.text
            symbol_markup = f'<kanji furigana="{furigana}">{symbol_markup}</kanji>'

        jp_markup += symbol_markup
    jp_markup = f'<{parent_tag}>{jp_markup}</{parent_tag}>'
    return jp_markup


def parse_vocab_page(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')

    vocab_tags = soup.findAll('div', attrs={'class': 'entry'})

    vocab_records = []
    for vocab_tag in vocab_tags:
        word = to_markup(list(vocab_tag.find("a").children))

        word_url = vocab_tag.find("a").get('href')
        url_split = word_url.replace('#a', '').split('/')
        [word_str, word_id] = [url_split[-1], int(url_split[-2])]

        translations = [x.strip() for x in
                        vocab_tag.find('div', attrs={'class': 'vocabulary-spelling'}).nextSibling.text.split(';')]

        use_count = int(vocab_tag.find(style='opacity: 0.5; margin-top: 1rem;').text)

        top_label = None
        top_label_tag = vocab_tag.find('div', attrs={'class': ['tag', 'tooltip']})
        if top_label_tag:
            top_label = top_label_tag.text

        vocab_records.append(
            {'markup': word, 'translations': translations, 'use_count': use_count, 'top_label': top_label,
             'word_str': word_str, 'word_id': word_id})
    return vocab_records


if __name__ == "__main__":
    pages_to_format = open_json("./out/persona_5314_vocab.txt")

    vocab = []
    for page in pages_to_format:
        vocab += parse_vocab_page(page)
        # break

    rewrite_file("./out/persona_5314_vocab.txt", vocab)
