#! /usr/bin/env python
import datetime
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity)

from authorization import requires_basic_auth
from user_json_schema import validate_user

app = Flask(__name__)
CORS(app)

## can also put in os.environ.get('SECRET')
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager(app)

""" Validation using Basic Authentication
Example of quickly using basic authentication approach when calling APIs.
"""


@app.route('/', methods=['GET'])
def api_hello():
    payload = {
        'method': request.method,
        'message': 'Hello World without any authentication.'
    }
    return jsonify(payload), 200


@app.route('/v1/ba/welcome', methods=['GET', 'POST'])
@requires_basic_auth
def api_ba_welcome():
    payload = {
        'method': request.method,
        'message': 'Return Welcome with basic authentication verified.'
    }
    return jsonify(payload), 200


""" Validation using JWT 
Example of quickly using JWT authentication approach when calling APIs.
"""


@app.route('/v1/jwt/user', methods=['POST'])
def api_auth_user():
    user = request.get_json()
    data = validate_user(user)
    if data['status']:
        data = data['data']
        ## Note: In prod, fetch from DB to check both username and password
        if user['email'] == 'email@email.com' and user['password'] == 'secret':
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            payload = {
                'method': request.method,
                'username': 'username',
                'password': 'secret',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return jsonify(payload), 200
        else:
            payload = {
                'method': request.method,
                'message': 'Invalid username or password.'
            }
            return jsonify(payload), 401

    payload = {
        'method': request.method,
        'message': 'Bad request parameters.'
    }
    return jsonify(payload), 400


@app.route('/v1/jwt/welcome', methods=['GET', 'POST'])
@jwt_required
def api_jwt_welcome():
    payload = {
        'method': request.method,
        'message': 'Return Welcome with jwt authentication verified.'
    }
    return jsonify(payload), 200


@app.route('/v1/jwt/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    payload = {
        'method': request.method,
        'token': create_access_token(identity=current_user)
    }
    return jsonify(payload), 200


port = int(os.getenv("PORT", 0))
if __name__ == '__main__':
    if port != 0:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()
