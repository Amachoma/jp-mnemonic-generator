import json

source_radicals = []
with open('../radicals.json', 'r') as source_radicals_file:
    for line in source_radicals_file:
        source_radicals.append(json.loads(line.strip()))

ru_radicals_file = open('../radicals_out_ru.json', 'r', encoding="utf-8")
ru_radicals = json.load(ru_radicals_file)

translation_dict = {}
for index in range(len(source_radicals)):
    translation_dict[source_radicals[index]["meaning"]] = ru_radicals[index]["meaning"]

with open('kanji_updated.json', 'r', encoding="utf-8") as kanji_updated_file:
    for line in kanji_updated_file:
        kanji_record = json.loads(line.strip())

        radicals_ru = list(map(lambda x: translation_dict[x], kanji_record["radicals"]))
        meaning_ru = kanji_record["meaning_ru"]
        character = kanji_record["character"]

        with open('kanji_mnemonic_gen.json', 'a', encoding="utf-8") as kanji_out:
            json.dump({"radicals_ru": radicals_ru, "meaning_ru": meaning_ru, "character": character}, kanji_out,
                      ensure_ascii=False)
            kanji_out.write('\n')
