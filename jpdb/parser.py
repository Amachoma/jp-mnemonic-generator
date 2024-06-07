import requests
import asyncio
from time import time
from bs4 import BeautifulSoup

from utils.file import open_json, open_lines, write_line
from utils.time import AvgRemainingTime
from utils.print_utils import draw_progress_bar


def download_kanji_pages():
    downloaded_data = [record['character'] for record in open_lines('out/raw_pages_all.txt')]

    levels = open_json("../levels.json")

    total_count = sum([len(level['kanji']) for level in levels])
    avg_timer = AvgRemainingTime(total=total_count - len(downloaded_data))

    for index in range(len(levels)):
        level = levels[index]
        for kanji_index in range(len(level['kanji'])):
            kanji = level['kanji'][kanji_index]
            if kanji['character'] in downloaded_data or kanji['character'] == "々":
                continue

            print(f"Processing {kanji['character']}")
            start_time = time()

            pages = {}
            sections = {'examples': 'e', 'vocab': 'v', 'kanji': 'k'}
            for [key, value] in sections.items():
                url = f"https://jpdb.io/kanji/{kanji['character']}?expand={value}#used_in_{kanji['character']}_{value}"
                page = requests.get(url)
                pages[key] = page.text
            write_line('out/raw_pages_all.txt', {"pages": pages, "character": kanji['character']})

            elapsed_time = time() - start_time
            avg_timer.add_item(elapsed_time)

            draw_progress_bar(avg_timer.percent)
            print(f"{avg_timer}\n\n\n")


# def process_page(page):
#     soup = BeautifulSoup(page, "html.parser")
#     frequency_table_tag = soup.find("table", attrs={'class': ['cross-table', 'label-right-align']})
#     print(frequency_table_tag)


def download_word_pages():
    word_links = open_lines("./out/vocab_links")

    finished_word_ids = [x["word_id"] for x in open_lines("./out/words_all.txt")]

    total_count = len(word_links) - len(finished_word_ids)

    avg_timer = AvgRemainingTime(total=total_count)

    for link in word_links:
        word_id = int(link.split("/")[-3])
        if word_id in finished_word_ids:
            continue

        print(f"Processing link '{link}'... ")
        start_time = time()

        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        write_line("./out/words_all.txt", {"page": str(soup.find("body")), "word_id": word_id})

        elapsed_time = time() - start_time
        avg_timer.add_item(elapsed_time)

        draw_progress_bar(avg_timer.percent)
        print(f"{avg_timer}\n\n\n")


if __name__ == "__main__":
    download_word_pages()
    # download_kanji_pages()
    # pages = open_lines("./out/raw_data.txt")
    # for page in pages:
    #     print(f"processing {page['character']}")
    #     process_page(page['html'])
    #     break