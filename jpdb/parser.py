import requests
from time import time

from utils.file import open_json, open_lines, write_line
from utils.time import AvgRemainingTime
from utils.print_utils import draw_progress_bar

if __name__ == "__main__":
    downloaded_data = [record['character'] for record in open_lines('./out/raw_data.txt')]

    levels = open_json("../levels.json")

    total_count = sum([len(level['kanji']) for level in levels])
    avg_timer = AvgRemainingTime(total=total_count - len(downloaded_data))

    for index in range(len(levels)):
        level = levels[index]
        for kanji_index in range(len(level['kanji'])):
            kanji = level['kanji'][kanji_index]
            if kanji['character'] in downloaded_data:
                continue

            print(f"Processing {kanji['character']}")
            start_time = time()

            page = requests.get(f"https://jpdb.io/vocabulary/1629200/{kanji['character']}/used-in")
            write_line('./out/raw_data.txt', {"html": page.text, "character": kanji['character']})

            elapsed_time = time() - start_time
            avg_timer.add_item(elapsed_time)

            draw_progress_bar(avg_timer.percent)
            print(f"{avg_timer}\n\n\n")
