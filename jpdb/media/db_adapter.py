import json

from utils.file import IndexReader

# [("JoJo's Bizarre Adventure", '544'),
# ('JoJo no Kimyou na Bouken: Stardust Crusaders - Egypt-hen', '7397'),
# ('JoJo no Kimyou na Bouken: Stardust Crusaders', '7345'),
# ('JoJo no Kimyou na Bouken: Ougon no Kaze', '7399'),
# ('JoJo no Kimyou na Bouken: Diamond wa Kudakenai', '7398')]

# Persona 5 - 5314

if __name__ == "__main__":
    def extend_media_index(record):
        json_record = json.loads(record)
        return {'id': json_record['id'], 'title': json_record['title'], 'genre': json_record['genre']}


    reader = IndexReader("../out/title_vocab.txt", index_gen_callback=extend_media_index)

    # jojo_record = reader.get(lambda x: x['id'] == '7398')
    # print(jojo_record['stats'])

    # sorted_vocab = sorted(persona_records[0]['title_vocab'], key=lambda x: x['frequency'], reverse=True)
    # for i in range(20, 30):
    #     print(sorted_vocab[i])

    video_games = reader.get(lambda x: x['genre'] == 'video game')
    # for game in video_games:
    #     print(game['title'])
    print(video_games[21]['stats'])

