import os
import site
import traceback

from flask import Flask, jsonify, request, session, Response
from flask_cors import CORS
from flask_restx import Api, Resource, reqparse
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

src_path = os.path.dirname(__file__)
pjt_home_path = os.path.join(src_path, os.pardir)
pjt_home_path = os.path.abspath(pjt_home_path)
site.addsitedir(pjt_home_path)

from utils.comn_logger import comn_logger
from models import model_ex1

FLASK_RUN_PORT = 55000
FLASK_DEBUG = True

# instantiate the app
app = Flask(__name__)
api = Api(app, version='1.0',
          title='Flask API',
          description='A simple Flask API',
          )

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# 환경변수 로딩
# os.environ
load_dotenv()


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name')

@app.route('/', methods=['GET'])
def test_router():
    msg = 'This is Docker Test development Server!'
    comn_logger.info(msg)
    return jsonify(msg)


@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify('good')


@app.route('/traceback_test', methods=['GET'])
def traceback_test_router():
    msg = 'ok'
    try:
        int('k')
    except:
        msg = traceback.format_exc()
        comn_logger.error(msg)
    return jsonify(msg)


@app.route('/api/model_ex1', methods=['POST'])
def run_model_ex1():
    params = request.get_json()
    x = params['x']
    y = params['y']
    result = model_ex1.model_simple(x, y)
    result_json = {'result': result}
    msg = str(result_json)
    comn_logger.info(msg)
    return jsonify(result_json)


@api.route('/hello')
class Hello(Resource):
    def get(self):
        return {'message': 'hello world'}


@api.route('/echo')
class Hello(Resource):
    def get(self):
        args = parser.parse_args()
        msg = args['name']
        return 'message > ' +  'echo: %s' % msg


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'), debug=os.environ.get('FLASK_DEBUG'))
    app.run(host='0.0.0.0', port=FLASK_RUN_PORT, debug=FLASK_DEBUG)
