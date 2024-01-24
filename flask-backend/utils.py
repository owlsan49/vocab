import json


etypes = {'0': 'unfamiliar_word', '1': 'new_word',
          '2': 'spelling_mistakes_word', '3': 'sin_plu_word'}

def read_json(data_path):
    try:
        with open(data_path, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
    except Exception as e:
        print(e)
        print(f'{data_path} is Null')
        data = None
    return data


def write_json(file_name, json_dict, mode='w'):
    with open(file_name, mode) as jf:
        json.dump(json_dict, jf)


def update_record(record, data, file_name):
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
