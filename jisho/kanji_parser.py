import json
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
from utils.print_utils import draw_progress_bar
from utils.file import open_lines, write_line, open_json

jisho_url = "https://jisho.org/search"
kanshudo_url = "https://www.kanshudo.com/kanji"


def not_empty(arr, message="Empty value encountered"):
    if len(arr) == 0:
        raise Exception(message)


def get_int(string):
    number_part = re.search(r'\d+', string)
    if number_part:
        return int(number_part.group())
    else:
        return None


def get_compounds(compounds):
    parsed_compounds = []
    for compound in compounds:
        compound_string = compound.text.replace('\n', '').strip()
        compound_pattern = re.compile(r"(.*)\s+【(.*)】\s+(.*)")
        match = compound_pattern.match(compound_string)
        if match:
            [c_kanji, c_reading, c_meaning] = [match.group(num).strip() for num in range(1, 4)]
            parsed_compounds.append({'kanji': c_kanji, 'reading': c_reading, 'meaning': c_meaning})
    return parsed_compounds if len(parsed_compounds) > 0 else None


def parse_kanji(kanji):
    web_page = requests.get(f"{jisho_url}/{kanji}%20%23kanji")
    doc = BeautifulSoup(web_page.text, "html.parser")

    kanji_details = doc.findAll("div", attrs={'class': ["kanji", "details"]})

    result = {}
    for kanji_section in kanji_details:
        kanji_character = kanji_section.find("h1", attrs={'class': "character"}).text

        if kanji_character != kanji:
            continue

        # MEANINGS
        main_meanings = [word.strip() for word in
                         kanji_section.find("div", attrs={'class': 'kanji-details__main-meanings'}).text.split(", ")]
        not_empty(main_meanings, "Main meanings are empty")
        result['main_meanings'] = main_meanings

        # READINGS
        readings_container = kanji_section.find(attrs={'class': 'kanji-details__main-readings'})

        kun_readings = [kun.strip() for kun in
                        (readings_container.find("dl", attrs={'class': ["dictionary_entry", "kun_yomi"]})
                         .find("dd", attrs={'class': 'kanji-details__main-readings-list'})).text.split("、")]
        on_readings = [on.strip() for on in
                       (readings_container.find("dl", attrs={'class': ["dictionary_entry", "on_yomi"]})
                        .find("dd", attrs={'class': 'kanji-details__main-readings-list'})).text.split("、")]
        [not_empty(x, "Main readings are empty") for x in [kun_readings, on_readings]]
        result['readings'] = {'on': on_readings, 'kun': kun_readings}

        # STATS
        kanji_stats = kanji_section.find("div", attrs={'class': 'kanji_stats'})

        stats = {}
        try:
            grade = get_int(kanji_stats.find("div", attrs={'class': 'grade'}).find("strong").text)
            stats['grade'] = grade
        except:
            stats['grade'] = None

        try:
            jlpt = kanji_stats.find("div", attrs={'class': 'jlpt'}).find("strong").text
            stats['jlpt'] = jlpt
        except:
            stats['jlpt'] = None

        try:
            frequency = get_int(kanji_stats.find("div", attrs={'class': 'frequency'}).find("strong").text)
            stats['frequency'] = frequency
        except:
            stats['frequency'] = None
        result['stats'] = stats

        # COMPOUNDS
        compounds = {}
        try:
            on_reading_compounds = get_compounds(
                kanji_section.find(string="On reading compounds").find_parent("div").findAll("li"))
            compounds["on"] = on_reading_compounds
        except:
            compounds["on"] = None

        try:
            kun_reading_compounds = get_compounds(
                kanji_section.find(string="Kun reading compounds").find_parent("div").findAll("li"))
            compounds["kun"] = kun_reading_compounds
        except:
            compounds["kun"] = None
        result["compounds"] = compounds

        return {'kanji': kanji_character, **result}


def parse_jisho():
    finished_kanji = [record['kanji'] for record in open_lines("./out/raw_data.txt")]

    characters_to_parse = []
    levels = open_json('../levels.json')
    for index in range(len(levels)):
        level = levels[index]
        for kanji in level['kanji']:
            if kanji["character"] not in finished_kanji and kanji['character'] != '々':
                characters_to_parse.append(kanji["character"])

    total_count = len(characters_to_parse)
    for index in range(total_count):
        character = characters_to_parse[index]

        draw_progress_bar(index / total_count)
        print(character)
        write_line('./out/raw_data.txt', parse_kanji(character))


def fill_missing_data(rec):
    print("\n\n")
    print(rec["kanji"])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html',
    }

    web_page = requests.get(f"{kanshudo_url}/{rec["kanji"]}", headers=headers)
    doc = BeautifulSoup(web_page.text, "html.parser")

    details_section = doc.find(attrs={'class': 'kdetails2'})

    try:
        jlpt_level = details_section.find(string="JLPT: ").parent.nextSibling.text
        rec["stats"]["jlpt"] = jlpt_level
    except:
        print(f"Unable to set jlpt level for {rec['kanji']}, skipping...")

    try:
        grade_level = details_section.find(string="Grade: ").parent.nextSibling.text
        rec["stats"]["grade"] = int(grade_level)
    except:
        print(f"Unable to set grade for {rec['kanji']}, skipping...")

    return rec


if __name__ == "__main__":
    jisho_raw = open_lines("./out/raw_data.txt")
    for record in jisho_raw:
        [with_grade, with_jlpt_level] = [record["stats"]["grade"], record["stats"]["jlpt"]]
        if not with_grade or not with_jlpt_level:
            write_line("./out/filled_data.txt", fill_missing_data(record))
        else:
            write_line("./out/filled_data.txt", record)
