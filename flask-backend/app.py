from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import (read_json, init_update, etypes, write_json,
                   records, gt_vocabs, record_path, update_record)

import shutil

app = Flask(__name__)
CORS(app)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    shutil.copy(record_path, f'bk_{record_path}')
    init_update(records, data, record_path)
    return jsonify({'resCode': 0})


@app.route('/get_vocab', methods=['GET'])
def get_vocab():
    unidf = request.args.get('unidf')
    sec_ids = unidf[-4:]
    print(sec_ids)
    results = {'resCode': 0}
    if unidf not in records.keys():
        results['msg'] = 'wrong unidf'
    elif sec_ids not in gt_vocabs.keys():
        results['msg'] = 'section id does not exist'
    else:

        record, error_words, refer_words = update_record(unidf, sec_ids)
        record['ew'] = error_words
        record['rw'] = refer_words
        results.update(record)
        print(record)
    return jsonify(results)


# @app.route('/correct', methods=['POST'])
# def post_correct():
#     data = request.get_json()
#     print(f"post_correct: {data}")
#
#     unidf = data['unidf']
#     results = {'resCode': 0}
#     if unidf not in records.keys():
#         results['msg'] = 'wrong unidf'
#     else:
#         shutil.copy(record_path, f'bk_{record_path}')
#         record = records[unidf]
#         record['unfamiliar_word'] = []
#         record['new_word'] = []
#         record['spelling_mistakes_word'] = []
#         record['sin_plu_word'] = []
#
#         record['corrected_word'] = data['correct_str'].split()
#         error_count = 0
#         for idx, word in enumerate(record['corrected_word']):
#             if '/' == word:
#                 record['corrected_word'][idx] = record['listening_word'][idx]
#             else:
#                 error_count += 1
#                 cword, etype = word.split('-')
#                 record['corrected_word'][idx] = cword
#                 record[etypes[etype]].append(cword)
#                 record['error_rate'] = error_count / record['word_len']
#                 record['unfamiliar_rate'] = len(record['unfamiliar_word']) / record['word_len']
#                 record['new_rate'] = len(record['new_word']) / record['word_len']
#                 record['spelling_mistakes_rate'] = len(record['spelling_mistakes_word']) / record['word_len']
#                 record['sin_plu_rate'] = len(record['sin_plu_word']) / record['word_len']
#
#         print(record)
#         records[unidf].update(record)
#         results.update(record)
#         write_json(record_path, records)
#     return results


if __name__ == '__main__':

    app.run(debug=True)
