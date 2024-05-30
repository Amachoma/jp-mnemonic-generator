import json
import requests
from bs4 import BeautifulSoup

from deep_translator import GoogleTranslator, MyMemoryTranslator

yarxi_url = "https://www.yarxi.ru/online/search.php"


def draw_progress_bar(progress):
    bar_length = 50
    completed_length = int(bar_length * progress)
    bar = '█' * completed_length + '-' * (bar_length - completed_length)

    percentage = progress * 100
    print(f'[{bar}] {percentage:.2f}% complete')


def get_yarxi_translation(kanji):
    page = requests.post(yarxi_url, data=f"K=&R={kanji}&M=&S=&D=0&NS=0&F=0",
                         headers={"Content-Type": "application/x-www-form-urlencoded"})
    doc = BeautifulSoup(page.text, "html.parser")
    translation = doc.find(attrs={'id': 'nick'})
    if translation is not None:
        return [elem.text for elem in translation.findAll("span")]
    else:
        print(f"Skipped: {kanji}")
        return None


source_kanji = []
with open('../kanji.json', 'r') as kanji_file:
    for line in kanji_file:
        source_kanji.append(json.loads(line.strip()))

source_characters = []
with open('../levels.json', 'r') as levels_file:
    levels = json.load(levels_file)

    for index in range(len(levels)):
        level = levels[index]
        for kanji in level['kanji']:
            source_characters.append(kanji["character"])

total_count = len(source_characters)
# for index in range(total_count):
#     percent_done = index / total_count
#     draw_progress_bar(percent_done)
#     kanji_character = source_characters[index]
#
#     kanji_record = source_kanji[index]
#     translation = get_yarxi_translation(kanji_character)
#
    # with open('kanji_updated.out', 'a', encoding="utf-8") as kanji_out:
    #     out.dump({**kanji_record, "meaning_ru": translation, "character": kanji_character}, kanji_out,
    #               ensure_ascii=False)
    #     kanji_out.write('\n')


# for word in get_yarxi_translation("経"):
#     print(word)

print(MyMemoryTranslator(source='english', target='russian').translate("keep it up, you are awesome"))