from utils.file import open_lines
from pprint import pprint

if __name__ == "__main__":
    jisho_records = open_lines("./out/raw_data.txt")
    freq_sorted = sorted(jisho_records,
                         key=lambda x: x['stats']['frequency'] if x['stats']['frequency'] is not None else float('inf'))

    for index in range(11):
        record = freq_sorted[index]
        print(f"================== TOP {index + 1} frequency ================")
        pprint(record)
        print("\n\n\n")
