import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint

from utils.kanji import get_kanji_levels
from utils.file import write_line, open_lines

kanshudo_url = "https://www.kanshudo.com/kanji"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html',
}


def login():
    login_url = 'https://www.kanshudo.com/users/sign_in'
    login_page = requests.get(login_url, headers=headers)
    soup = BeautifulSoup(login_page.text, "html.parser")

    authenticity_token = soup.find("input", attrs={'name': 'authenticity_token'}).get('value').strip()
    login_response = requests.post(login_url, data={
        'authenticity_token': authenticity_token,
        'user[email]': 'fotiga5869@fincainc.com',
        'user[password]': '_t4HQNGNx9Q#_zc',
        'user[remember_me]': '0',
        'commit': 'Log in'
    }, headers=headers, cookies=login_page.cookies)

    if login_response.status_code == 200:
        return login_response.cookies
    else:
        raise Exception("Failed to login")


def parse_page(web_page):
    doc = BeautifulSoup(web_page, "html.parser")
    stat_keys = ['Strokes\n        :', 'Frequency:', 'JLPT: ', 'Usefulness: ', 'Grade: ']

    stats = {}
    for key in stat_keys:
        formatted_key = key.replace(':', '').strip().lower()
        stats[formatted_key] = None

        span_text = doc.find(string=key)
        if span_text:
            value = span_text.parent.nextSibling.text.strip()
            try:
                stats[formatted_key] = int(value)
            except:
                stats[formatted_key] = value

    word_sections = doc.findAll("div", attrs={"class": 'jukugorow'})
    words = []
    for section in word_sections:
        word_record = {"readings": {"group": None, "kanji_word": None, "furigana": None}}

        word_container = section.find(attrs={'class': 'jukugo'})
        reading_contents = word_container.contents[1].contents

        # READINGS
        try:
            reading_group = ''.join(
                [re.sub(r'\s+', ' ', x.text.replace('\n', '').strip()) for x in
                 section.findPreviousSibling(attrs={'class': 'halfspaced'}).contents[:-2]]
            )
            word_record['readings']['group'] = reading_group
        except:
            pass

        kanji_word = section.find("div", attrs={'class': 'f_kanji'}).text
        word_furigana = section.find("div", attrs={'class': 'furigana'}).text

        if len(reading_contents) > 1:
            ending = reading_contents[-1].text
            kanji_word += ending
            word_furigana += ending

        word_record['readings']['kanji_word'] = kanji_word
        word_record['readings']['furigana'] = word_furigana

        # STATS
        word_stats = {'jlpt': None, 'usefulness': None}
        class_name_regex = r"^.*_(\d+)$"

        jlpt_container = section.find(attrs={'class': 'jlpt_container'})
        if jlpt_container:
            jlpt_class_name = jlpt_container.contents[1].get('class')[0]

            match = re.match(class_name_regex, jlpt_class_name)
            word_stats['jlpt'] = f'N{match.group(1)}'

        usefulness_container = section.find(attrs={'class': re.compile("^ja-ufn_\\d+$")})
        if usefulness_container:
            usefulness_class_name = usefulness_container.get('class')[0]
            match = re.match(class_name_regex, usefulness_class_name)
            word_stats['usefulness'] = int(match.group(1))

        word_record['stats'] = word_stats

        word_groups = []
        for row in section.findAll(attrs={'class': 'vm'}):
            word_group = {"classification": None, "words": None, "details": None}

            vm_id = row.find(attrs={'class': 'vm_id'})
            if vm_id:
                vm_id.extract()

            contains_classification = row.contents[0].name == "div"
            if contains_classification:
                word_group["classification"] = [x.strip() for x in row.contents[0].text.split(",")]
                word_group["words"] = [x.strip() for x in row.contents[1].text.split(';')]

            else:
                word_group["classification"] = word_groups[-1]['classification']
                word_group["words"] = [x.strip() for x in row.contents[0].text.split(';')]

            if row.contents[-1].name == "span":
                word_group["details"] = row.contents[-1].text[1:-1]
            word_groups.append(word_group)

        word_record['translations'] = word_groups
        words.append(word_record)
    return {"main_stats": stats, "words": words}


if __name__ == "__main__":
    raw_html = open_lines("./out/raw_html.txt")

    levels = get_kanji_levels()
    kanji_index = -1
    for level in levels:
        for kanji in level['kanji']:
            kanji_index += 1
            if kanji['character'] == "々":
                continue
            # print(kanji['character'])
            formatted_record = {**parse_page(raw_html[kanji_index]), "kanji": kanji}
            write_line("./out/raw_formatted.txt", formatted_record)
