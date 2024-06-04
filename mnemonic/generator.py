from enum import Enum
import xml.dom.minidom

from py_generative.ai import ChatBot
from utils.file import open_lines, write_line
from utils.time import AvgRemainingTime
from utils.print_utils import draw_progress_bar


class RunMode(Enum):
    AUTO = 1
    INTERACTIVE = 2


class MnemonicGenerator:
    def __init__(self, dataset_path, output_path):
        self.dataset_path = dataset_path
        self.output_path = output_path

    def run(self, mode=RunMode.AUTO, print_process=False):

        kanji_to_skip = []
        try:
            kanji_to_skip = [x['character'] for x in open_lines(self.output_path)]
        except:
            print("Output file is not present. Generating mnemonics from scratch")

        mnemonics_dataset = open_lines(self.dataset_path)
        avg_timer = AvgRemainingTime(total=len(mnemonics_dataset) - len(kanji_to_skip))
        mnemonic_ai = ChatBot()

        for kanji_gen_record in mnemonics_dataset:
            if kanji_gen_record['character'] in kanji_to_skip:
                continue

            if print_process:
                print(f"====== Processing '{kanji_gen_record['character']}' ======\n")

            message = f'''Попробуй сгенерировать мнемонику для следующего набора данных: {kanji_gen_record['radicals_ru']}, {kanji_gen_record['meanings_ru']}, '{kanji_gen_record['character']}'''
            [mnemonic, time_elapsed] = mnemonic_ai.send_message(message)

            avg_timer.add_item(time_elapsed)

            if mode == RunMode.AUTO:
                write_line(self.output_path, {"mnemonic": mnemonic, "character": kanji_gen_record["character"]})

                if print_process:
                    draw_progress_bar(avg_timer.percent)
                    print(avg_timer)
                    print("\n\n\n")

            elif mode == RunMode.INTERACTIVE:
                user_input = ""
                message_history = [message]
                while user_input != "y":
                    print(f'Значения иероглифа: {kanji_gen_record['meanings_ru']}\n Радикалы: {kanji_gen_record['radicals_ru']}')
                    message_history.append(mnemonic)
                    dom = xml.dom.minidom.parseString(mnemonic)
                    print(dom.toprettyxml())

                    user_input = input("Accept this mnemonic? y/n/exit\n You can also write extra details here to "
                                       "correct mnemonic:\n")

                    if user_input == "y":
                        write_line(self.output_path, {"mnemonic": mnemonic, "character": kanji_gen_record["character"]})
                    elif user_input == "n":
                        [mnemonic, _] = mnemonic_ai.send_message(message)
                        message_history = [message]
                    elif user_input == "exit":
                        exit()
                    else:
                        message_history.append(user_input)
                        [mnemonic, _] = mnemonic_ai.send_message(user_input, message_history)



