import json
import pprint


def convert_to_utf8(input_file, output_file):
    try:
        # Чтение данных из файла в кодировке Unicode
        with open(input_file, 'r', encoding='utf-8') as file:
            data = file.read()

        output_data = json.loads(data)
        json_string = json.dumps(output_data, ensure_ascii=False)

        # # Запись данных в файл в кодировке UTF-8
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(json_string)

        print(f"Данные успешно перекодированы в UTF-8 и записаны в файл '{output_file}'.")

    except Exception as e:
        print(f"Возникла ошибка: {e}")


convert_to_utf8("translated_radicals.json", "converted_radicals.json")