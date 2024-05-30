from bs4 import BeautifulSoup
import requests
import json

URL = 'https://www.wanikani.com/'


def get_html_body(symbol):
    page = requests.get(URL + 'kanji/' + symbol)
    doc = BeautifulSoup(page.text, "html.parser")
    return doc.body


def get_radicals(html_body):
    radicals_dict = {}
    svg_radical_count = 0
    radicals_section = html_body.find("section", "subject-section subject-section--components")
    radicals_array = radicals_section.find_all("div", "subject-character__content")
    for radical in radicals_array:
        radical_character = radical.find("span", "subject-character__characters").text.strip()
        if radical_character == "":
            radical_character = 'svg_radical_{0}'.format(svg_radical_count)
            svg_radical_count += 1
        radical_meaning = radical.find("span", "subject-character__meaning").text.strip()
        radicals_dict[radical_character] = radical_meaning
    return radicals_dict


def get_meanings(html_body, main_kanji, radicals):
    radicals_reversed = {meaning.lower(): radical for radical, meaning in radicals.items()}
    marked_words = []
    meaning_dict = {}

    meaning_section = html_body.find("section", "subject-section subject-section--meaning")
    meaning_subsections = meaning_section.find_all("section", "subject-section__subsection")
    meanings_array = meaning_subsections[0].find_all("div", "subject-section__meanings")
    for meaning in meanings_array:
        meaning_title = meaning.find("h2", "subject-section__meanings-title").text.strip()
        meaning_items = meaning.find_all("p", "subject-section__meanings-items")
        for meaning_item in meaning_items:
            meaning_dict[meaning_title] = [item.strip() for item in meaning_item.text.split(',')]

    mnemonic_text = meaning_subsections[1].find("p", "subject-section__text")
    mnemonic_string_array = [str(radical) for radical in mnemonic_text.contents]
    meaning_dict["mnemonic"] = mnemonic_string_array

    mnemonic_array = mnemonic_text.find_all("mark")
    for item in mnemonic_array:
        if item["title"] == "Radical":
            marked_words.append([radicals_reversed[item.text.strip().lower()], item.text.strip().lower(), "radical"])
        else:
            marked_words.append([main_kanji, item.text.strip().lower(), "kanji"])

    hint_aside = meaning_subsections[1].find("aside", "subject-hint")
    hint_text = hint_aside.find("p", "subject-hint__text").text.strip()
    meaning_dict["hint"] = hint_text
    return meaning_dict


def get_similar_subjects(html_body):
    similar_subjects_array = []

    similar_subjects_section = html_body.find("section", "subject-section subject-section--similar-subjects")
    if similar_subjects_section is None:
        return None

    similar_subjects = similar_subjects_section.find_all("li", "subject-character-grid__item")
    for similar_subject in similar_subjects:
        similar_subject_character = similar_subject.find("span", "subject-character__characters").text.strip()
        similar_subject_reading = similar_subject.find("span", "subject-character__reading").text.strip()
        similar_subject_meaning = similar_subject.find("span", "subject-character__meaning").text.strip()
        similar_subjects_array.append({"kanji": similar_subject_character, "reading": similar_subject_reading, "meaning": similar_subject_meaning})
    return similar_subjects_array


def parse_kanji(kanji_string):
    result = []

    for kanji in kanji_string:
        body = get_html_body(kanji)
        radicals = get_radicals(body)
        meanings = (get_meanings(body, kanji, radicals))
        similar_subjects = get_similar_subjects(body)
        if similar_subjects is not None:
            result.append({"radicals": radicals, "meaning": meanings, "similar": similar_subjects})
        else:
            result.append({"radicals": radicals, "meaning": meanings})

    return result


def get_characters(doc, type):
    irregular_count = 0
    radicals = []
    for item in doc.find_all(attrs={'class': f"subject-character--{type}"}):
        radical = {'character': '', 'meaning': ''}
        character = item.find(attrs={'class': "subject-character__characters"})

        if character.text:
            radical['character'] = character.text
        else:
            radical['character'] = character.find(attrs={'src': True})['src']
            irregular_count += 1

        radical['meaning'] = item.find(attrs={'class': 'subject-character__meaning'}).text

        radicals.append(radical)
        print(radical)
    print(f"Parsed {len(radicals)} total. Irregular count: {irregular_count}")
    return radicals


def get_vocab(doc):
    words = []
    for item in doc.find_all(attrs={'class': "subject-character--vocabulary"}):
        words.append({
            'kanji': item.find(attrs={'class': "subject-character__characters"}).text,
            'reding': item.find(attrs={'class': "subject-character__reading"}).text,
            'meaning': item.find(attrs={'class': "subject-character__meaning"}).text
        })
    return words


def get_level(level):
    page = requests.get(f"{URL}/level/{level}")
    doc = BeautifulSoup(page.text, "html.parser")

    radicals = get_characters(doc, type="radical")
    kanji = get_characters(doc, type="kanji")
    words = get_vocab(doc)

    return {'radicals': radicals, 'kanji': kanji, 'words': words}


if __name__ == '__main__':
    levels = []

    # for level in range(1, 61):
    #     levels.append(get_level(level))
    #
    # with open('levels.out', 'w') as json_file:
    #     out.dump(levels, json_file)


page = requests.get(f"https://www.wanikani.com/radicals/arrow")
doc = BeautifulSoup(page.text, "html.parser")

print(doc.find("p", attrs={'class': 'subject-section__text'}).text)