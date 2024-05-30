from utils.file import open_lines


def group_by_jlpt():
    jlpt_sorted = {'N5': [], 'N4': [], "N3": [], "N2": [], "N1": [], "unspecified": []}
    jisho_records = open_lines("./out/raw_data.txt")

    for record in jisho_records:
        jlpt_level = record["stats"]["jlpt"]
        jlpt_sorted[jlpt_level if bool(jlpt_level) else "unspecified"].append(record)

    return jlpt_sorted


def group_by_grade():
    pass


if __name__ == "__main__":
    pass

