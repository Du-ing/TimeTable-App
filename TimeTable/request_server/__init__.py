from flask import Flask, request, jsonify
from flask_cors import CORS
from crawl_data import get_data, get_user

app = Flask(__name__)
CORS(app, suport_credentials=True)


@app.route('/')
def index():
    return '服务器正常运行'


@app.route('/getInfo')
def get_info():
    return jsonify({
        'status': 200,
        'msg': '查询成功',
        'data': {
            'is_updated': False,
            'downloadURL': '',
            'start_date': [2020, 8, 7],
        }
    })


@app.route('/getuser')
def request_user():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        user = get_user(username, password)
    except Exception as e:
        with open('error.log', 'w+', encoding='utf8') as fp:
            fp.write(str(e))
        return jsonify({
            'status': 500,
            'msg': '查询失败',
            'user': {}
        })

    return jsonify({
        'status': 200,
        'msg': '查询成功',
        'user': user
    })


@app.route('/api/lesson')
def request_data():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        data = get_data(username, password)
    except Exception as e:
        with open('error.log', 'w+', encoding='utf8') as fp:
            fp.write(str(e))
        return jsonify({
            'status': 500,
            'msg': '查询失败',
            'data': []
        })

    return jsonify({
        'status': 200,
        'msg': '查询成功',
        'data': data
    })


if __name__ == '__main__':
    app.run()