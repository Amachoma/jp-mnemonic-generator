from bs4 import BeautifulSoup
import requests
import json

URL = "https://www.wanikani.com/"
yarxi_url = "https://www.yarxi.ru/online/search.php"


def get_yarxi_translation(kanji):
    page = requests.post(yarxi_url, data=f"K=&R={kanji}&M=&S=&D=0&NS=0&F=0",
                         headers={"Content-Type": "application/x-www-form-urlencoded"})
    doc = BeautifulSoup(page.text, "html.parser")
    translation = doc.find(attrs={'id': 'nick'}).text
    if translation is not None:
        return translation
    else:
        raise Exception("Error", "No translation found")

def parse_kanji(kanji):
    page = requests.get(f"{URL}/kanji/{kanji}")
    doc = BeautifulSoup(page.text, "html.parser")

    radicals = []
    for radical_tag in doc.find_all(attrs={'class': 'subject-character--radical'}):
        radicals.append(radical_tag.find(attrs={'class': 'subject-character__info'}).text.strip())

    meaning_mnemonic = {'text': '', 'hint': ''}
    meaning = doc.find(attrs={'class': 'subject-section--meaning'})
    meaning_mnemonic['text'] = meaning.find(attrs={'class': 'subject-section__text'}).text.strip()

    meaning_mnemonic_hint = meaning.find(attrs={'class': 'subject-hint__text'})
    if meaning_mnemonic_hint:
        meaning_mnemonic['hint'] = meaning_mnemonic_hint.text.strip()

    reading_mnemonic = {'text': '', 'hint': ''}
    reading = doc.find(attrs={'class': 'subject-section--reading'})
    reading_mnemonic['text'] = reading.find(attrs={'class': 'subject-section__text'}).text.strip()

    reading_mnemonic_hint = reading.find(attrs={'class': 'subject-hint__text'})
    if reading_mnemonic_hint:
        reading_mnemonic['hint'] = reading_mnemonic_hint.text.strip()

    readings = {}
    for reading_tag in doc.find_all(attrs={'class': 'subject-readings__reading'}):
        reading_type = reading_tag.find(attrs={'class': 'subject-readings__reading-title'}).text.strip().replace("’",
                                                                                                                 '').lower()
        reading_items = reading_tag.find(attrs={'class': 'subject-readings__reading-items'}).text.strip()

        if reading_items != 'None':
            readings[reading_type] = reading_items.split(', ')

    words = []
    for item in doc.find_all(attrs={'class': 'subject-character--vocabulary'}):
        character = item.find(attrs={'class': 'subject-character__characters'}).text.strip()
        reading = item.find(attrs={'class': 'subject-character__reading'}).text.strip()
        meaning = item.find(attrs={'class': 'subject-character__meaning'}).text.strip()
        words.append({'character': character, 'reading': reading, 'meaning': meaning})

    return {'radicals': radicals, 'readings': {**readings, 'mnemonic': reading_mnemonic}, 'words': words,
            'meaning': {'mnemonic': meaning_mnemonic}}


with open('levels.json', 'r') as json_file:
    levels = json.load(json_file)

    for index in range(len(levels)):
        print(f"=================== Processing level {index + 1}...========================".upper())
        level = levels[index]
        for kanji in level['kanji']:
            print(kanji["character"])
            print(get_yarxi_translation(kanji["character"]))
            break
            # print(f"Processing kanji: {kanji['character']}")
            # kanji_dict = parse_kanji(kanji['character'])
            # with open('kanji.out', 'a') as kanji_file:
            #     out.dump(kanji_dict, kanji_file)
            #     kanji_file.write('\n')
        break
