import json

from flask import Blueprint, Flask, request, Response
from flask_cors import CORS

from categories import Categories

wb = Blueprint('wb', __name__)
CORS(wb)

categories = Categories.from_file('categories-tree.json')


@wb.route('/tags', methods=['GET'])
def get_tags():
    if request.method != 'GET':
        return Response(
            json.dumps({'status': 'error', 'message': 'Method not allowed.'}),
            status=405
        )

    data = request.args
    query = data['query']
    res = categories.find_by_category('кейп')
    print(res)

    return Response(
        json.dumps({'status': 'ok', 'data': res}, ensure_ascii=False).encode('utf8'),
        status=200,
        content_type='application/json; charset=utf-8'
    )    


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(wb, url_prefix='')
    app.run(host='0.0.0.0', port=8080, debug=True)
