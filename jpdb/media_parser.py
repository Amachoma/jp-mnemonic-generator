import math

import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import re
from time import time

from utils.file import open_lines, write_line
from utils.time import AvgRemainingTime
from utils.print_utils import draw_progress_bar
from jpdb.formatters import get_word_str


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, link)) for link in urls]
        responses = await asyncio.gather(*tasks)
        return responses


class AsyncFetcher:
    def __init__(self, max_parallel_requests):
        self.max_parallel_requests = max_parallel_requests

    def get(self, urls):
        result = []
        while len(urls) > 0:
            [current_urls, urls] = [urls[:self.max_parallel_requests], urls[self.max_parallel_requests:]]
            fetch_res = asyncio.run(fetch_all(current_urls))
            result += fetch_res
        return result


def parse_media(page):
    media = []
    media_tags = page.findAll('div', style="display: flex; flex-wrap: wrap;")
    for tag in media_tags:
        genre = tag.find("div", style="opacity: 0.5").text.lower()
        title = tag.find('h5').text
        use_count = int(tag.find('td').text)
        media_id = int(tag.find('a').get('href').split('/')[2])
        media.append({'genre': genre, 'title': title, 'use_count': use_count, 'media_id': media_id})
    return media


if __name__ == "__main__":
    finished_record_ids = [x['record_id'] for x in open_lines("./out/media_dataset.txt")]

    words_list = open_lines("./out/words_formatted.txt")
    avg_timer = AvgRemainingTime(total=len(words_list))
    for record in words_list:
        start_time = time()
        media_records = [{**media, **{'word_id': record['word_id'], 'word_str': record['word_str']}} for media in
                         record['media']]
        for m in media_records:
            record_id = f'm{m['media_id']}w{m['word_id']}'
            if record_id in finished_record_ids:
                continue
            write_line("./out/media_dataset.txt", {**m, "record_id": record_id})

        avg_timer.add_item(time() - start_time)
        draw_progress_bar(avg_timer.percent)
        print(avg_timer)
        print("\n\n\n")

    # finished_words = [x for x in open_lines("./out/media_urls.txt")]
    # print(sum([len(word['page_urls']) for word in finished_words]))

    # words = open_lines("./out/words_all.txt")
    #
    # avg_timer = AvgRemainingTime(total=len(words) - len(finished_words))
    # for word_page in words:
    #     if word_page['word_id'] in finished_words:
    #         continue
    #
    #     start_time = time()
    #     page_soup = BeautifulSoup(word_page['page'], 'html.parser')
    #     word_str = get_word_str(page_soup)
    #     word_page_link = f"https://jpdb.io/vocabulary/{word_page['word_id']}/{word_str}/used-in"
    #     print(f"Processing #{word_page['word_id']} {word_str}...")
    #
    #     total_count_tag = page_soup.find("p", style='opacity: 0.75; text-align: right;')
    #     if total_count_tag:
    #         page_count = math.ceil(int(re.findall(r'\d+', total_count_tag.text)[-1]) / 50)
    #
    #         if page_count > 1:
    #             page_urls = [f'{word_page_link}?offset={page_num * 50}' for page_num in range(1, page_count)]
    #             write_line("./out/media_urls.txt",
    #                        {'word_str': word_str, 'word_id': word_page['word_id'], 'page_urls': page_urls})
    #     avg_timer.add_item(time() - start_time)
    #     draw_progress_bar(avg_timer.percent)
    #     print(avg_timer)

    # fetcher = AsyncFetcher(5)

    # avg_timer = AvgRemainingTime(total=len(words) - len(finished_words))
    # for word in words:
    #     if word['word_id'] in finished_words:
    #         continue
    #
    #     print(f"Processing {word['word_id']}...")
    #     start_time = time()
    #
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #     }
    #     word_page_link = f"https://jpdb.io/vocabulary/{word['word_id']}/{word['word_str']}/used-in"
    #     page = requests.get(f"{word_page_link}", headers=headers)
    #
    #     page_soup = BeautifulSoup(page.text, "html.parser")
    #     word_media = parse_media(page_soup)
    #
    #     total_count_tag = page_soup.find("p", style='opacity: 0.75; text-align: right;')
    #     if total_count_tag:
    #         page_count = math.ceil(int(re.findall(r'\d+', total_count_tag.text)[-1]) / 50)
    #
    #         if page_count > 1:
    #             next_page_urls = [f'{word_page_link}?offset={page_num * 50}' for page_num in range(1, page_count)]
    #             if next_page_urls:
    #                 media_records = [parse_media(BeautifulSoup(x, "html.parser")) for x in fetcher.get(next_page_urls)]
    #                 word_media += media_records
    #
    #     write_line("./out/media-dataset.txt",
    #                {'word_id': word['word_id'], 'word_str': word['word_str'], 'media': word_media})
    #     avg_timer.add_item(time() - start_time)
    #     draw_progress_bar(avg_timer.percent)
    #     print(avg_timer)
