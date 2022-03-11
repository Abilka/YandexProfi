import flask
from flask import Flask

from db import DB

app = Flask(__name__)

BAD_REQUEST = flask.Response(status=400)

@app.route("/promo", methods=['POST'])
def post_promo():
    data = flask.request.json
    if data and data.get("name"):
        return str(DB().new_promo(data['name'], data.get('description') or ''))
    else:
        return BAD_REQUEST


@app.route("/promo/<int:id>/prize", methods=['POST'])
def post_prize(id):
    data = flask.request.json
    if data and data.get("description"):
        return str(DB().new_prize(id, data.get('description')))
    else:
        return BAD_REQUEST

@app.route("/promo/<int:id>/participant", methods=['POST'])
def new_participant(id):
    data = flask.request.json
    if data and data.get('name'):
        return flask.Response(str(DB().new_participant(data['name'], id)), status=200)
    else:
        return BAD_REQUEST

@app.route("/promo", methods=['GET'])
def get_promo():
    return flask.Response(str(DB().get_promo()), status=200)


@app.route("/promo/<int:id>", methods=['GET'])
def info_promo(id):
    return flask.Response(str(DB().info_promo(id)), status=200)


@app.route("/promo/<int:id>", methods=['PUT'])
def put_promo(id):
    data = flask.request.json
    if data and (data.get("name")) and data.get('name') != '':
        return str(DB().change_promo(data['name'], data.get('description') or '', id))
    else:
        return BAD_REQUEST


@app.route("/promo/<int:id>", methods=['DELETE'])
def del_promo(id):
    DB().del_promo(id)
    return flask.Response(status=200)




app.run(port=8080)
