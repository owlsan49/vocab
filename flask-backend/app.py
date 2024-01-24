from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import read_json, update_record, etypes

app = Flask(__name__)
CORS(app)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    update_record(records, data, record_path)
    return jsonify({'resCode': 0})


@app.route('/get_vocab', methods=['GET'])
def get_vocab():
    unidf = request.args.get('unidf')
    results = {'resCode': 0}
    if unidf not in records.keys():
        results['msg'] = 'wrong unidf'
    else:
        record = records[unidf]
        results.update(record)
        print(record)
    return jsonify(results)


@app.route('/correct', methods=['POST'])
def post_correct():
    data = request.get_json()
    print(f"post_correct: {data}")

    unidf = data['unidf']
    results = {'resCode': 0}
    if unidf not in records.keys():
        results['msg'] = 'wrong unidf'
    else:
        record = records[unidf]
        corrected_word = data['correct_str'].split('')
        error_count = 0
        for idx, word in enumerate(corrected_word):
            if '/' == word:
                record['corrected_word'][idx] = record['listening_word'][idx]
            else:
                error_count += 1
                cword, etype = word.split('-')
                record['corrected_word'].append(cword)
                record[etypes[etype]].append(cword)
                record['error_rate'] = error_count / record['word_len']
                record['unfamiliar_rate'] = len(record['unfamiliar_word']) / record['word_len']
                record['new_rate'] = len(record['new_word']) / record['word_len']
                record['spelling_mistakes_rate'] = len(record['spelling_mistakes_word']) / record['word_len']
                record['sin_plu_rate'] = len(record['sin_plu_word']) / record['word_len']
        print(record)
    return results


if __name__ == '__main__':
    record_path = r'C:\Users\13634\Documents\WPSDrive\learning-record.json'
    records = read_json(record_path)
    app.run(debug=True)