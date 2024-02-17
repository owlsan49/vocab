import json
import shutil
import re

etypes = {'0': 'unfamiliar_word', '1': 'new_word',
          '2': 'spelling_mistakes_word', '3': 'sin_plu_word'}
record_path = r'learning-record.json'
gt_path = r'processed_gt.json'


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
    gap_idx = unidf.find('c')
    date_str = unidf[:gap_idx]
    date = '-'.join(date_str[i:i + 2] for i in range(0, len(date_str), 2))
    section = unidf[gap_idx:]
    data['listening_word'] = data['listening_word'].replace("\n", "  ")
    data['listening_word'] = re.split(r' {2,}', data['listening_word'])
    record[unidf] = {
        'date': date,
        'section': section,
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
        'ew': [],
        'rw': [],
        'mean': [],
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
    meanings = []

    record['corrected_word'] = corrected_vocabs['gt_vocabs']
    error_count = 0
    print(len(record['corrected_word']), len(record['listening_word']))
    for idx, word in enumerate(record['corrected_word']):
        # print(record['listening_word'][idx], word)
        lw = record['listening_word'][idx]
        lw = lw.replace('=', ' ')
        word = word.replace('’', '\'')
        word_cvb = word.split('=')
        if lw not in word_cvb:
            # print(error_count)
            error_count += 1
            error_words.append(lw)
            refer_words.append(word)
            meanings.append(corrected_vocabs['meaning'][idx])

            record['unfamiliar_word'].append(word)
            record['error_rate'] = error_count / record['word_len']
            record['unfamiliar_rate'] = len(record['unfamiliar_word']) / record['word_len']
            record['new_rate'] = len(record['new_word']) / record['word_len']
            record['spelling_mistakes_rate'] = len(record['spelling_mistakes_word']) / record['word_len']
            record['sin_plu_rate'] = len(record['sin_plu_word']) / record['word_len']

    records[unidf].update(record)
    records[unidf]['ew'] = error_words
    records[unidf]['rw'] = refer_words
    records[unidf]['mean'] = meanings
    write_json(record_path, records)
    return record
