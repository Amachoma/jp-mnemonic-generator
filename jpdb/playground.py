import json

from utils.file import open_json, IndexReader

if __name__ == "__main__":
    nekopara_vocab = open_json('./out/persona_5314_vocab.txt')


    def extend_media_index(record):
        json_record = json.loads(record)
        return {'id': json_record['id'], 'title': json_record['title']}

    reader = IndexReader("./out/flat_media_records.txt",
                         index_gen_callback=extend_media_index)
    nekopara_words = reader.get(lambda x: x['id'] == '5314')['words']
    nekopara_word_ids = [x['word_id'] for x in nekopara_words]

    filtered_vocab = list(filter(lambda x: x['word_id'] not in nekopara_word_ids, nekopara_vocab))

    print(len(nekopara_vocab))
    print(len(nekopara_word_ids))
    print(len(filtered_vocab))

    for word in filtered_vocab:
        print(word)
