import json
import re

source_mnemonics = []
with open("mnemonic_gen.json", encoding="utf-8") as mnemonic_file:
    for line in mnemonic_file:
        source_mnemonics.append(line.strip())

source_kanji = []
with open("kanji_mnemonic_gen.json", encoding="utf-8") as kanji_mnemonic_file:
    for line in kanji_mnemonic_file:
        source_kanji.append(json.loads(line.strip()))

source_radicals = json.load(open("radicals_out (10).json", encoding="utf-8"))
radical_list = {d["meaning"]: d["character"] for d in source_radicals}

db_data = []
for index in range(len(source_mnemonics)):
    kanji_record = source_kanji[index]

    kanji = {'character': kanji_record['character'], 'label': kanji_record['meaning_ru']}
    radicals = [{"character": radical_list[r], "label": r} for r in kanji_record['radicals_ru']]
    mnemonic = source_mnemonics[index][1: -1]

    match = re.search("^```xml(.*)```$", mnemonic)
    if match:
        mnemonic = match.group(1)

    mnemonic = " ".join(mnemonic.replace('\\n', '').strip().split())

    db_data.append({"kanji": kanji, "radicals": radicals, "mnemonic": mnemonic})

with open('db_data_out.json', 'w', encoding='utf-8') as out:
    json.dump({"version": 1, 'collection': db_data}, out, ensure_ascii=False)
