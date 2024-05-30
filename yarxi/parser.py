import requests
from bs4 import BeautifulSoup

yarxi_url = "https://www.yarxi.ru/online/search.php"


def get_yarxi_translation(kanji):
    page = requests.post(yarxi_url, data=f"K=&R={kanji}&M=&S=&D=0&NS=0&F=0",
                         headers={"Content-Type": "application/x-www-form-urlencoded"})
    doc = BeautifulSoup(page.text, "html.parser")
    translation = doc.find(attrs={'id': 'nick'})
    if translation is not None:
        return [elem.text for elem in translation.findAll("span")]
    else:
        return None


if __name__ == "__main__":
    print(get_yarxi_translation("率"))
