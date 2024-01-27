import json
import shutil

etypes = {'0': 'unfamiliar_word', '1': 'new_word',
          '2': 'spelling_mistakes_word', '3': 'sin_plu_word'}
record_path = r'learning-record.json'
gt_path = 'processed_gt.json'


def read_json(data_path):
    try:
        with open(data_path, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
    except Exception as e:
        print(e)
        print(f'{data_path} is Null')
        data = {}
    return data


def write_json(file_name, json_dict, mode='w'):
    with open(file_name, mode) as jf:
        json.dump(json_dict, jf)


records = read_json(record_path)
gt_vocabs = read_json(gt_path)


def init_update(record, data, file_name):
    unidf = data['unidf']
    data['listening_word'] = data['listening_word'].replace("\n", " ").split()
    record[unidf] = {
        'date': data['date'],
        'section': data['section'],
        'listening_word': data['listening_word'],
        'word_len': len(data['listening_word']),
        'corrected_word': [],
        'unfamiliar_word': [],
        'unfamiliar_rate': 0.,
        'new_word': [],
        'new_rate': 0.,
        'spelling_mistakes_word': [],
        'spelling_mistakes_rate': 0.,
        'sin_plu_word': [],
        'sin_plu_rate': 0.,
        'error_rate': 0.,
    }
    print(record[unidf])
    write_json(file_name, record)


def update_record(unidf, sec_ids):
    corrected_vocabs = gt_vocabs[sec_ids]
    shutil.copy(record_path, f'bk_{record_path}')
    record = records[unidf]
    record['unfamiliar_word'] = []
    record['new_word'] = []
    record['spelling_mistakes_word'] = []
    record['sin_plu_word'] = []

    error_words = []
    refer_words = []

    record['corrected_word'] = corrected_vocabs['gt_vocabs']
    error_count = 0
    for idx, word in enumerate(record['corrected_word']):
        # print(record['listening_word'][idx], word)
        if record['listening_word'][idx] != word:
            # print(error_count)
            error_count += 1
            error_words.append(record['listening_word'][idx])
            refer_words.append(word)

            record['unfamiliar_word'].append(word)
            record['error_rate'] = error_count / record['word_len']
            record['unfamiliar_rate'] = len(record['unfamiliar_word']) / record['word_len']
            record['new_rate'] = len(record['new_word']) / record['word_len']
            record['spelling_mistakes_rate'] = len(record['spelling_mistakes_word']) / record['word_len']
            record['sin_plu_rate'] = len(record['sin_plu_word']) / record['word_len']

    records[unidf].update(record)
    write_json(record_path, records)
    return record, error_words, refer_words
