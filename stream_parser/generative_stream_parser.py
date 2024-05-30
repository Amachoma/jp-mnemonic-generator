import os
from dotenv import load_dotenv
import subprocess

from py_generative.ai import ChatBot
from utils.file import open_lines, write_line
from utils.time import AvgRemainingTime
from utils.print_utils import draw_progress_bar

load_dotenv()
url = "https://api.promptpark.jp/questions"
headers = {"Authorization": f"Bearer {os.getenv('ID_TOKEN')}"}

CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''


def notify(title, text):
    subprocess.call(['osascript', '-e', CMD, title, text])


if __name__ == "__main__":
    user_input = input("Input 'y' to start mnemonic generation: ")

    if user_input.lower() != 'y':
        exit(0)

    kanji_to_skip = []
    try:
        kanji_to_skip = [x['character'] for x in open_lines("./mnemonic_gen.json")]
    except:
        print("Output file is not present. Generating mnemonics from scratch")

    mnemonics_dataset = open_lines('./mnemonic_dataset.txt')
    avg_timer = AvgRemainingTime(total=len(mnemonics_dataset) - len(kanji_to_skip))
    mnemonic_ai = ChatBot()

    for kanji_gen_record in mnemonics_dataset:
        if kanji_gen_record['character'] in kanji_to_skip:
            continue

        print(f"====== Processing '{kanji_gen_record['character']}' ======\n")

        message = f'''Попробуй сгенерировать мнемонику для следующего набора данных: {kanji_gen_record['radicals_ru']}, {kanji_gen_record['meanings_ru']}, '{kanji_gen_record['character']}'''
        [mnemonic, time_elapsed] = mnemonic_ai.send_message(message)

        avg_timer.add_item(time_elapsed)

        draw_progress_bar(avg_timer.percent)
        print(avg_timer)
        print("\n\n\n")

        write_line('./mnemonic_gen.json', {"mnemonic": mnemonic, "character": kanji_gen_record["character"]})
