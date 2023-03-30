import os
import site
import traceback

from flask import Flask, jsonify, request, session, Response
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

src_path = os.path.dirname(__file__)
pjt_home_path = os.path.join(src_path, os.pardir)
pjt_home_path = os.path.abspath(pjt_home_path)
site.addsitedir(pjt_home_path)

from utils.comn_logger import comn_logger
from models import model_ex1

# instantiate the app
app = Flask(__name__)

# 환경변수 로딩
# os.environ
load_dotenv()


@app.route('/', methods=['GET'])
def test_router():
    msg = 'This is Docker Test development Server!'
    comn_logger.info(msg)
    return jsonify(msg)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'), debug=os.environ.get('FLASK_DEBUG'))
