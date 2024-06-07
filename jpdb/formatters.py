from bs4 import BeautifulSoup

from utils.file import open_lines, write_line

if __name__ == "__main__":
    kanji_dataset = open_lines("out/raw_pages_all.txt")

    url_to_process = set()
    for record in kanji_dataset:
        [examples, vocab, kanji] = [record["pages"]['examples'], record["pages"]['vocab'], record["pages"]['kanji']]

        examples_section = BeautifulSoup(examples, "html.parser").find(attrs={'class': 'subsection-examples'})
        vocab_section = BeautifulSoup(vocab, "html.parser").find(attrs={'class': 'subsection-used-in'})
        kanji_section = BeautifulSoup(kanji, "html.parser").find(attrs={'class': 'subsection-composed-of-kanji'})

        vocab_tags = vocab_section.findAll(attrs={'class': 'used-in'})
        for tag in vocab_tags:
            url_split = [x.encode("latin-1").decode("utf-8") for x in tag.find("a").get("href").split("/")[2:-1]]
            word_id = int(url_split[0])
            converted_url = "/".join(url_split)
            word_url = f"https://jpdb.io/vocabulary/{converted_url}/used-in"
            url_to_process.add(word_url)

    print(len(url_to_process))
    for url in url_to_process:
        write_line("./out/vocab_links", url)
