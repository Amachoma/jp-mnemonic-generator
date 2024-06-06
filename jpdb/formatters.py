from bs4 import BeautifulSoup

from utils.file import open_lines

if __name__ == "__main__":
    kanji_dataset = open_lines("./out/raw_pages.txt")
    for record in kanji_dataset:
        [examples, vocab, kanji] = [record["pages"]['examples'], record["pages"]['vocab'], record["pages"]['kanji']]

        examples_section = BeautifulSoup(examples, "html.parser").find(attrs={'class': 'subsection-examples'})
        vocab_section = BeautifulSoup(examples, "html.parser").find(attrs={'class': 'subsection-used-in'})
        kanji_section = BeautifulSoup(examples, "html.parser").find(attrs={'class': 'subsection-composed-of-kanji'})

        print(kanji_section)
        break
