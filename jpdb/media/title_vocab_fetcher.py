import math

from bs4 import BeautifulSoup
import requests
import re

from utils.fetcher import AsyncFetcher
from utils.file import write_line, open_lines, IndexReader, continuous_writer
from utils.string import to_snake_case
from utils.number import to_number
from jpdb.utils import to_character_markup


def fetch_title_page(media_id, title, genre):
    genre_label = genre.replace(' ', '-').replace('book-(non-fiction)', 'non-fiction').replace("aozora-bunko",
                                                                                               "aozora").replace(
        'audio-work', 'audio')
    title_url = f'https://jpdb.io/{genre_label}/{media_id}/'

    page_text = requests.get(title_url).text
    soup = BeautifulSoup(page_text, 'html.parser')

    title_stat_tag = soup.find("div",
                               style="margin-left: 0.5rem; display: flex; flex-direction: column; flex-grow: 1; align-items: flex-start;")

    title_stats = {}
    for table_row in title_stat_tag.findAll("tr"):
        [label, value] = list(table_row.children)

        title_stats[to_snake_case(label.text)] = value.text
    title_stats['vocab_link'] = title_stat_tag.find('a', style='margin: 0; margin-top: 0.5rem;').get('href')

    chapter_info_tags = soup.findAll("div", style="padding-left: 1rem; padding-right: 1rem; margin-bottom: 2rem;")

    chapters = []
    for chapter_info_tag in chapter_info_tags:
        chapter_title = chapter_info_tag.previousSibling.text

        stats = {}
        for table_row in chapter_info_tag.findAll("tr"):
            [label, value] = list(table_row.children)
            stats[to_snake_case(label.text)] = to_number(value.text.replace('%', ''))

        vocab_link = chapter_info_tag.find('a').get('href')
        chapters.append({'title': chapter_title, 'stats': stats, 'vocab_link': vocab_link})

    return {'id': media_id, 'title': title, 'genre': genre, 'stats': title_stats, 'chapters': chapters}


def fetch_title_details():
    # TODO: It's better to rewrite this code using continuous_writer if it'll be reused
    finished_titles = [x['id'] for x in open_lines('../out/title_details.txt')]

    title_vocab_records = open_lines("../out/flat_media_records.txt")

    for title_record in title_vocab_records:
        if title_record['id'] in finished_titles:
            continue
        print(f'Processing {title_record['genre'].replace(' ', '-')}/{title_record['id']}...')
        media_details = fetch_title_page(title_record['id'], title_record['title'], title_record['genre'])
        write_line('../out/title_details.txt', media_details)


def fetch_chapter_vocab(vocab_link):
    chapter_vocab_link = f"https://jpdb.io{vocab_link}"
    page = requests.get(chapter_vocab_link,
                        headers={'Content-Type': 'text/html; charset=utf-8', 'Accept-Charset': 'utf-8'})

    soup = BeautifulSoup(page.text.encode('iso-8859-1').decode('utf-8'), 'html.parser')

    entries_count_tag = soup.find(style='opacity: 0.75; text-align: right;')
    word_count = int(re.findall(r'\d+', entries_count_tag.text)[-1])
    print(f"Processing chapter with {word_count} words")

    def get_vocab_words(soup_object):
        words = []
        word_tags = soup_object.findAll("div", {'class': 'entry'})
        for word_tag in word_tags:
            [word_details_tag, word_frequency_tag] = list(word_tag.children)
            frequency = int(word_frequency_tag.text) if word_frequency_tag.text else None

            word_markup = to_character_markup(word_details_tag.findAll('ruby'))

            rating = None
            rating_tag = word_details_tag.find(attrs={'class': 'tags xbox'})
            if rating_tag is not None:
                rating = rating_tag.text

            translations = [x.strip() for x in
                            word_tag.find('div', attrs={'class': 'vocabulary-spelling'}).nextSibling.text.split(';')]
            words.append(
                {'markup': word_markup, 'translations': translations, 'frequency': frequency, 'rating': rating})

        return words

    vocab_links = [f'{chapter_vocab_link}?offset={page * 50}' for page in range(1, math.ceil(word_count / 50))]
    async_fetcher = AsyncFetcher(delay_between_requests=0.4)

    first_page_words = get_vocab_words(soup)
    words = [*first_page_words, *[x for y in async_fetcher.get(vocab_links,
                                                               after_callback=lambda response: get_vocab_words(
                                                                   BeautifulSoup(response, 'html.parser'))) for x in y]]

    return words


def fetch_chapters():
    def process_title_record(record):
        chapters = record['chapters']

        extended_title_record = {**record}
        if chapters:
            extended_chapters = []
            for chapter in chapters:
                words = fetch_chapter_vocab(chapter['vocab_link'])
                extended_chapters.append({**chapter, 'words': words})
                extended_title_record['chapters'] = extended_chapters
        else:
            vocab_all = fetch_chapter_vocab(record['stats']['vocab_link'])
            extended_title_record['title_vocab'] = vocab_all
        return extended_title_record

    continuous_writer(in_path='../out/title_details.txt', out_path='../out/title_vocab.txt',
                      processing_callback=process_title_record)


if __name__ == "__main__":
    fetch_chapters()
    # fetch_title_details()
