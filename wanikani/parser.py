import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator, MyMemoryTranslator

from wanikani.collection import WanikaniCollection
from kanshudo.collection import KanshudoCollection
from utils.file import write_line, open_lines

if __name__ == "__main__":
    # url = f'https://www.wanikani.com/radicals'
    # kanshudo_col = KanshudoCollection()
    # n5_kanji = kanshudo_col.group_by_jlpt()["N5"]
    # wanikani_col = WanikaniCollection()
    #
    # n5_wanikani_records = [wanikani_col.get_kanji(record.kanji) for record in n5_kanji]
    #
    # radicals = set()
    # for record in n5_wanikani_records:
    #     for radical in record.radicals:
    #         radicals.add(radical)
    #
    # for radical in radicals:
    #     print(f'Processing {radical}')
    #     request = requests.get(f'{url}/{'-'.join([x.lower() for x in radical.split(" ")])}')
    #     write_line("./out/n5_radicals.txt", request.text)
    pages = open_lines("./out/n5_radicals.txt")
    for page in pages:
        soup = BeautifulSoup(page)

        radical = soup.find(attrs={'class': 'page-header__title-text'})
        mnemonic = soup.find(attrs={'class': 'subject-section__text'})

        print(f'Processing {radical.text}')
        translated = GoogleTranslator(source='english', target='russian').translate(mnemonic.text)
        write_line('./out/n5_radical_mnemonics_ru.txt', {'mnemonic_ru': translated, 'radical': radical.text})
