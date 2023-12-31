import asyncio
import sys
from os import path, getcwd

import typer
from flask import Flask, request
from flask_cors import cross_origin, CORS

from backend.service.service import add_quiz_group, \
    get_quizzes_groups, delete_quiz_group, update_quiz_group, get_statistic
from backend.init import init_models
import logging
from flask import jsonify

logging.basicConfig(level=logging.INFO)

sys.path.append(getcwd())
cli = typer.Typer()
app = Flask(__name__)

CORS(app, support_credentials=True)
logging.getLogger('flask_cors').level = logging.DEBUG


@app.route("/")
async def hello1():
    return "API v1.0"


@app.route('/getQuizGroup', methods=['GET'])
async def get_quiz_group_http():
    quizzes_groups = await get_quizzes_groups()
    return jsonify(quizzes_groups)


@app.route('/upload.do', methods=['POST'])
async def get_photo_http():
    return 'picture'


@app.route('/getStatistic', methods=['GET'])
async def get_stat_http():
    statistic = await get_statistic()
    return jsonify(statistic)


@app.route('/addQuizGroup', methods=['POST'])
async def add_quiz_group_http():
    req_data = request.get_json(force=True)
    quiz_group = req_data['quizGroup']
    await add_quiz_group(quiz_group)
    return quiz_group


@app.route('/updateQuizGroup', methods=['POST'])
async def update_quiz_group_http():
    req_data = request.get_json(force=True)
    quiz_group = req_data['quizGroup']
    await update_quiz_group(quiz_group)
    return quiz_group


@app.route('/deleteQuizGroup', methods=['DELETE'])
async def delete_quiz_group_http():
    req_data = request.get_json(force=True)
    req_id = req_data['id']
    await delete_quiz_group(req_id)
    return req_id


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request. %s', e)
    return "An internal error occurred", 500


@cli.command()
def db_init_models():
    asyncio.run(init_models())


if __name__ == '__main__':
    if __package__ is None:
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    app.run(debug=True)
    # cli()
