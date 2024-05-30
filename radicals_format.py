import json
import re


def is_english(text):
    return all(ord(char) < 128 for char in text)


source_radicals = []
with open('radicals.json', 'r') as radicals_file:
    for line in radicals_file:
        source_radicals.append(json.loads(line.strip()))


mnemonic_pattern1 = r'"mnemonic": "(.*?)"'
mnemonic_pattern2 = r'"mnemonic": "(.*?)»'

pattern = r'"meaning": "(.*?)"'
translated_radicals = []
with open('radicals_ru.json', 'r', encoding="utf-8") as radicals_file:
    for line_number, line in enumerate(radicals_file, start=0):
        res = {}
        match = re.search(pattern, line)
        if match:
            value = match.group(1)
            res["meaning"] = value

        match = re.search(mnemonic_pattern1, line)
        match1 = re.search(mnemonic_pattern2, line)
        if match:
            res["mnemonic"] = match.group(1)
        elif match1:
            res["mnemonic"] = match1.group(1)
        else:
            print("Не распарсил мнемонику")

        translated_radicals.append({"character": source_radicals[line_number]["character"], **res})

# with open('translated_radicals.out', 'w') as translated_file:
#     out.dump(translated_radicals, translated_file)
