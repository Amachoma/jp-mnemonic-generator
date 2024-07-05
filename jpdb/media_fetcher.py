from bs4 import BeautifulSoup
from time import time

from jpdb.formatters import get_word_str, get_media_records
from utils.fetcher import AsyncFetcher
from utils.file import open_lines, open_json, write_line, rewrite_file
from utils.time import AvgRemainingTime
from utils.print_utils import draw_progress_bar


def get_media_by_url(page, word_id):
    soup = BeautifulSoup(page, 'html.parser')

    word_str = get_word_str(soup)
    media_records = get_media_records(soup)

    return [{**rec, **{"word_id": word_id, "word_str": word_str}} for rec in media_records]


if __name__ == "__main__":
    pass
    # base_url = f"https://jpdb.io/video-game/5314/persona-5/vocabulary-list"
    # async_fetcher = AsyncFetcher(delay_between_requests=0.4)
    #
    # fetched_pages = async_fetcher.get([f'{base_url}?offset={page*50}' for page in range(482)])
    # rewrite_file("./out/persona_5314_vocab.txt", fetched_pages)

    # media_pages = [get_media_by_url(page, record['word_id']) for page in async_fetcher.get(url_for_download)]

    # # finished_word_ids = [x["word_id"] for x in open_lines("./out/extra_media_record.txt")]
    # meta = open_json('./out/media_fetcher_last_id.txt')
    #
    # url_records = open_lines("./out/media_urls.txt")
    # # url_count = sum([len(record['page_urls']) for record in url_records])
    # async_fetcher = AsyncFetcher(delay_between_requests=0.4)
    #
    # avg_timer = AvgRemainingTime(len(url_records))
    # is_already_parsed = True
    # finished_count = 0
    # for record in url_records:
    #     if is_already_parsed:
    #         finished_count += 1
    #         if record['word_id'] == meta['word_id']:
    #             is_already_parsed = False
    #             avg_timer.processed_count = finished_count
    #         continue
    #
    #     print(f'Processing #{record['word_id']}: {record['word_str']}({len(record['page_urls'])})...')
    #     url_for_download = record['page_urls']
    #     start_time = time()
    #     media_pages = [get_media_by_url(page, record['word_id']) for page in async_fetcher.get(url_for_download)]
    #
    #     item_count = 0
    #     for media_page in media_pages:
    #         for media_rec in media_page:
    #             write_line("./out/extra_media_record.txt", media_rec)
    #             item_count += 1
    #     rewrite_file("./out/media_fetcher_last_id.txt", {'word_id': record['word_id']})
    #
    #     avg_timer.add_item(time() - start_time)
    #     draw_progress_bar(avg_timer.percent)
    #     print(avg_timer)
    #     print('\n\n\n')
