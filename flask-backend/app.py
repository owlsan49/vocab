from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import (read_json, init_update, etypes, write_json,
                   records, gt_vocabs, record_path, update_record,
                   check_port_in_use)

import shutil
import random

app = Flask(__name__)
CORS(app)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    shutil.copy(record_path, f'bk_{record_path}')
    init_update(records, data, record_path)
    return jsonify({'resCode': 0})


@app.route('/init_info', methods=['GET'])
def init_info():
    results = {'resCode': 0, 'last_info': []}
    rec_keys = list(records.keys())
    for rk in rec_keys[-10:]:
        results['last_info'].append(records[rk])
    return jsonify(results)


@app.route('/get_vocab', methods=['GET'])
def get_vocab():
    unidf = request.args.get('unidf')
    sec_ids = unidf[unidf.find('c'):]
    print(sec_ids)
    update = request.args.get('update')
    results = {'resCode': 0}
    if unidf not in records.keys():
        results['msg'] = 'wrong unidf'
    elif update == 'false':
        record = records[unidf]
        random.seed(42)
        random.shuffle(record['rw'])
        random.seed(42)
        random.shuffle(record['mean'])
        results.update(record)
        print(f'2: {results}')
    elif sec_ids not in gt_vocabs.keys():
        results['msg'] = 'section id does not exist'
    else:
        print(f'update: {unidf}')
        record = update_record(unidf, sec_ids)
        results.update(record)

    return jsonify(results)


if __name__ == '__main__':
    port = read_json('../config.json')['port']
    app.run(debug=True, port=port)
