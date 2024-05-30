import json


def open_lines(path):
    result = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            if data:
                result.append(data)
    return result


def write_line(path, line):
    with open(path, 'a', encoding="utf-8") as file:
        json.dump(line, file, ensure_ascii=False)
        file.write('\n')


def open_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
