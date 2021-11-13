import json

from flask import Blueprint, Flask, request, Response
from flask_cors import CORS

from categories import Categories, NonProduct

wb = Blueprint('wb', __name__)
CORS(wb)

categories = Categories.from_file('categories-tree.json')
nonproduct = NonProduct.from_file('nonproductqueries.json')

@wb.route('/tags', methods=['GET'])
def get_tags():
    if request.method != 'GET':
        return Response(
            json.dumps({'status': 'error', 'message': 'Method not allowed.'}),
            status=405
        )

    data = request.args
    query = data['query']
    # query = "поддержка"

    is_non_product, res = nonproduct.check_is_non_product(query)

    if is_non_product:
        return Response(
            json.dumps({'status': 'ok', 'data': [res]}, ensure_ascii=False).encode('utf8'),
            status=200,
            content_type='application/json; charset=utf-8'
        )

    # тут давид

    res = categories.find_by_category('кейп')

    return Response(
        json.dumps({'status': 'ok', 'data': res}, ensure_ascii=False).encode('utf8'),
        status=200,
        content_type='application/json; charset=utf-8'
    )    


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(wb, url_prefix='')
    app.run(host='0.0.0.0', port=8080, debug=True)
