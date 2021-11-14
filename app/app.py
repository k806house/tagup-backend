import json
import random
import itertools

from flask import Blueprint, Flask, request, Response
from flask_cors import CORS

from categories import Categories, NonProduct
from tags import TagGenerator

wb = Blueprint('wb', __name__)
CORS(wb)

categories = Categories.from_file('categories-tree.json')
nonproduct = NonProduct.from_file('nonproductqueries.json')
tg = TagGenerator('../models/word2vec_clean5.model')

@wb.route('/tags', methods=['GET'])
def get_tags():
    if request.method != 'GET':
        return Response(
            json.dumps({'status': 'error', 'message': 'Method not allowed.'}),
            status=405
        )

    data = request.args
    query = data['query']

    is_non_product, res = nonproduct.check_is_non_product(query)

    if is_non_product:
        return Response(
            json.dumps({'status': 'ok', 'data': [res]}, ensure_ascii=False).encode('utf8'),
            status=200,
            content_type='application/json; charset=utf-8'
        )

    # stage 1: matching query in tree
    direct_matches = direct_query_matching(query)

    # stage 2: get suggests
    suggests = tg.generate(query)

    # stage 3: matching suggests in tree
    suggest_matches = direct_suggest_matching(suggests[0])

    # merge matches from tree
    tree_matches = direct_matches + suggest_matches
    suggest_count = min(7, len(suggests[0]) + len(suggests[1]))
    response = result_proccess(tree_matches, suggests, suggest_max_count=suggest_count)

    print(response)
    return Response(
        json.dumps({'status': 'ok', 'data': response}, ensure_ascii=False).encode('utf8'),
        status=200,
        content_type='application/json; charset=utf-8'
    )


def direct_query_matching(query):
    query_split = query.split()
    for token in query_split:
        matches = categories.find_by_category(token)
        if matches:
            return matches
    return []


def direct_suggest_matching(suggests):
    for suggest in suggests:
        query, _ = suggest
        matches = categories.find_by_category(query)
        if matches:
            return matches
    return []


def result_proccess(tree_matches, suggests,
                    suggest_max_count=7, tags_count=10):
    # если в дереве нашли меньше 3 матчей, то увеличиваем suggest_max_count
    # чтобы в сумме tree_count и suggest_max_count давали 10
    tree_max_count = tags_count - suggest_max_count
    tree_count = len(tree_matches)
    if tree_count < tree_max_count:
        suggest_max_count = tags_count - tree_count

    # если в саджестах больше suggest_max_count матчей,
    # обрезаем его
    suggests_merged = []
    for i, j in itertools.zip_longest(suggests[0], suggests[1]):
        if i is not None:
            suggests_merged.append(i)
        if j is not None:
            suggests_merged.append(j)

    suggest_count = len(suggests_merged)
    if suggest_count > suggest_max_count:
        suggests_merged = suggests_merged[:suggest_max_count]
        suggest_count = suggest_max_count

    suggest_names = [i[0] for i in suggests_merged]

    # если есть соседние категории в листе, то берем их
    # если нет, то берем категории по пути к корню
    # пока не наберем нужное количество
    result = []
    match_count = tags_count - suggest_count
    cur = 0
    while cur < match_count:
        if not tree_matches:
            break

        match_in_tree = random.choice(tree_matches)

        if match_in_tree['siblings'] is not None:
            random.shuffle(match_in_tree['siblings'])
            siblings_shuffle = match_in_tree['siblings']
            for i in siblings_shuffle:
                if cur >= match_count:
                    break

                if i != match_in_tree['match'] and i.lower() not in suggest_names:
                    result.append(i)
                    cur += 1
        else:
            for i in reversed(match_in_tree['path']):
                if cur >= match_count:
                    break

                if i != match_in_tree['match'] and i.lower() not in suggest_names:
                    result.append(i)
                    cur += 1

        del match_in_tree

    response = []
    for suggest in suggests_merged:
        name, _ = suggest
        response.append({
            'tag': name.lower(),
            'isRouting': False,
            'ref': ''
        })

    for name in result:
        response.append({
            'tag': name.lower(),
            'isRouting': False,
            'ref': ''
        })

    return response


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(wb, url_prefix='')
    app.run(host='0.0.0.0', port=8080, debug=True)
