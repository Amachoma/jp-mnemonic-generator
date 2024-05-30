import json
import xml.dom.minidom

source_mnemonics = []
with open("mnemonic_gen.json", encoding="utf-8") as mnemonic_file:
    for line in mnemonic_file:
        source_mnemonics.append(line.strip())

source_kanji = []
with open("kanji_updated.json", encoding="utf-8") as kanji_file:
    for line in kanji_file:
        source_kanji.append(json.loads(line.strip()))

for index in range(len(source_mnemonics)):
    xml_markup = f'''<?xml version= "1.0" ?>{source_mnemonics[index][9:-6]}'''

    xml_obj = xml.dom.minidom.parseString(xml_markup)
    print(xml_obj.toprettyxml())
    print(
        f'rads: {source_kanji[index]["radicals"]}, meaning: {source_kanji[index]["meaning_ru"]}, char: {source_kanji[index]["character"]}')

    input("Press to continue")
    print("\n\n\n")
