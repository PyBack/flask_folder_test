import os
import site
import traceback

from logging.config import dictConfig

from flask import Blueprint
from flask import Flask, jsonify, request, session, Response
from flask_cors import CORS
from flask_restx import Api, Resource, Namespace, reqparse
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

# Flask root logger config
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s [%(levelname)s] %(filename)s %(lineno)d: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# instantiate the app
app = Flask(__name__)
blueprint = Blueprint('api_2', __name__, url_prefix='/api/v2')
api = Api(blueprint, version='0.2',
          title='Flask API',
          description='Flask API Structure Test',
          )

app.register_blueprint(blueprint)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# 환경변수 로딩
# os.environ
load_dotenv()


@app.route('/', methods=['GET'])
def test_router():
    msg = 'This is Docker Test development Server!'
    comn_logger.info(msg)
    print(msg)
    return jsonify(msg)


@app.route('/health_check', methods=['GET'])
def health_check():
    comn_logger.info('flaskapi: good')
    print('flaskapi: good')
    return jsonify({'flaskapi': 'good'})


@app.route('/traceback_test', methods=['GET'])
def traceback_test_router():
    msg = 'ok'
    try:
        int('k')
    except:
        msg = traceback.format_exc()
        app.logger.error(msg)
    return jsonify(msg)


@app.route('/api/model_ex1', methods=['POST'])
def run_model_ex1():
    params = request.get_json()
    x = params['x']
    y = params['y']
    result = model_ex1.model_simple(x, y)
    result_json = {'result': result}
    msg = str(result_json)
    app.logger.info(msg)
    return jsonify(result_json)


@api.route('/hello')
class Hello(Resource):
    def get(self):
        app.logger.info('hello world')
        return {'message': 'hello world'}


@api.route('/echo')
class Echo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='Name')

    @api.expect(parser)
    def get(self):
        args = self.parser.parse_args()
        msg = args['name']
        app.logger.info(msg)
        return 'message > ' + 'echo: %s' % msg

# # ex_ns_v2 = Namespace('example', 'example service v2')
# api.add_namespace(ex_ns_v2)
# ex_ns_v2.add_resource(Echo)
# ex_ns_v2.add_resource(Hello)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'), debug=os.environ.get('FLASK_DEBUG'))
    app.run(host='0.0.0.0', port=FLASK_RUN_PORT, debug=FLASK_DEBUG)
