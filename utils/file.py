import json
import os


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


class IndexReader:
    def __init__(self, file_path, index_gen_callback=None):
        is_file_exists = os.path.exists(file_path)
        if not is_file_exists:
            raise ValueError("File not found")

        self.file_path = file_path
        self.index_gen_callback = index_gen_callback

        path_split = file_path.split("/")

        filename = path_split.pop()
        [name, extension] = filename.split(".")

        index_file_path = "/".join([*path_split, f'{name}.index'])
        self.index_file_path = index_file_path

        is_index_file_exists = os.path.exists(index_file_path)
        if not is_index_file_exists:
            self._create_index()

    def _create_index(self):
        index_ranges = []
        prev_position = 0
        with open(self.file_path, 'rb') as file:
            # skip first line
            file.readline()

            while True:
                new_position = file.tell()
                line = file.readline()

                new_record = {"range": (prev_position, new_position)}
                prev_position = new_position

                if line:
                    if self.index_gen_callback:
                        try:
                            additional_data = self.index_gen_callback(line.decode())
                            if additional_data:
                                new_record = {**new_record, **additional_data}
                        except:
                            raise ValueError("Custom index generation callback is not correct")
                    index_ranges.append(new_record)
                else:
                    break
        print(index_ranges)
        # write_line(self.index_file_path, index_ranges)


if __name__ == "__main__":
    reader = IndexReader("../jpdb/out/raw_data.txt", index_gen_callback=lambda record: {'character': json.loads(record)['character']})