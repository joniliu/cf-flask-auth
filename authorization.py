from functools import wraps

from flask import request, jsonify


def check_auth(username, password):
    ## Note: In prod, use DB to store both username and password
    return username == 'username' and password == 'secret'


def authenticate():
    payload = {
        'method': request.method,
        'message': 'Return basic authentication required.'
    }
    return jsonify(payload), 401


def requires_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
