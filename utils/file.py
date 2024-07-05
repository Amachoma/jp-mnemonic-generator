import json
import os
import types

from utils.print_utils import draw_progress_bar
from utils.time import AvgRemainingTime
import importlib

time = importlib.import_module('time').time


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


def rewrite_file(path, content):
    with open(path, 'w', encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False)


def open_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


class IndexReader:
    def __init__(self, file_path, index_gen_callback=None, getter_callback=lambda line: json.loads(line)):
        is_file_exists = os.path.exists(file_path)
        if not is_file_exists:
            raise ValueError("File not found")

        self.file_path = file_path
        self.index_gen_callback = index_gen_callback
        self.getter_callback = getter_callback

        path_split = file_path.split("/")

        filename = path_split.pop()
        [name, extension] = filename.split(".")

        index_file_path = "/".join([*path_split, f'{name}.index'])
        self.index_file_path = index_file_path

        is_index_file_exists = os.path.exists(index_file_path)
        if not is_index_file_exists:
            self._create_index()
        else:
            self.index_data = open_json(index_file_path)

    def _create_index(self):
        index_ranges = []
        with open(self.file_path, 'rb') as file:
            while True:
                new_position = file.tell()
                line = file.readline()

                new_record = {"start_byte": new_position}

                if line:
                    if self.index_gen_callback:
                        additional_data = self.index_gen_callback(line.decode())
                        if not additional_data:
                            raise ValueError("Index generation callback hasn't returned a value")
                        else:
                            if type(additional_data) is dict:
                                new_record = {**new_record, **additional_data}
                            else:
                                raise ValueError('Index generation callback returned value other then dict')
                    index_ranges.append(new_record)
                else:
                    break
        rewrite_file(self.index_file_path, index_ranges)
        self.index_data = index_ranges

    def get(self, getter):
        if isinstance(getter, types.FunctionType):
            result = list(filter(getter, self.index_data))

            if len(result) == 1:
                start_byte = result[0]['start_byte']

                with open(self.file_path, 'rb') as file:
                    file.seek(start_byte)
                    line = file.readline()

                    return self.getter_callback(line.decode())

            elif len(result) > 1:
                results = []
                for match in result:
                    start_byte = match['start_byte']
                    with open(self.file_path, 'rb') as file:
                        file.seek(start_byte)
                        line = file.readline()
                        results.append(self.getter_callback(line.decode()))
                return results
            else:
                raise IndexError('Record not found')
        elif (type(getter)) in [str, int]:
            index = int(getter)
            record = self.index_data[index]
            if record is None:
                raise IndexError(f"Index out of range: f{index}/{len(self.index_data)}")
            start_byte = record['start_byte']

            with open(self.file_path, 'rb') as file:
                file.seek(start_byte)
                line = file.readline()

                return self.getter_callback(line.decode())
        else:
            raise TypeError("Provided getter type is not supported")

    def __len__(self):
        return len(self.index_data)


def continuous_writer(in_path, out_path, processing_callback):
    print("Starting continuous writer...")
    reader = IndexReader(in_path)

    in_path_split = in_path.split("/")
    filename = in_path_split.pop()
    [name, extension] = filename.split(".")
    cursor_file_path = "/".join([*in_path_split, f'{name}.cursor'])

    is_cursor_exists = os.path.exists(cursor_file_path)
    if not is_cursor_exists:
        rewrite_file(cursor_file_path, -1)

    cursor_index = open_json(cursor_file_path)

    print("Initialization finished successfully")

    timer = AvgRemainingTime(len(reader), cursor_index + 1)
    for index in range(cursor_index + 1, len(reader)):
        start_time = time()
        payload = processing_callback(reader.get(index))
        write_line(out_path, payload)

        cursor_index += 1
        rewrite_file(cursor_file_path, cursor_index)
        timer.add_item(time() - start_time)

        draw_progress_bar(timer.percent)
        print(timer)

    print("Finished!")


if __name__ == "__main__":
    def extend_media_index(record):
        json_record = json.loads(record)
        return {'id': json_record['id'], 'title': json_record['title']}


    reader = IndexReader("../jpdb/out/flat_media_records.txt",
                         index_gen_callback=extend_media_index)

    genre_counters = {}
    for i in range(6662):
        rec = reader.get(i)
        genre = rec['genre']
        genre_counters[genre] = genre_counters.get(genre, 0) + 1
