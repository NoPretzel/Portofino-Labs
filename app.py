import time

import redis
from flask import Flask, jsonify, request, Response
from datetime import datetime
from functools import wraps

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def save_ip_hit(ip, path):
    retries = 5
    while True:
        try:
            cache.rpush('ip:{}path:{}'.format(ip, path), datetime.now().timestamp())
            break
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/v1/hello-world')
def hello_world():
    ip = request.remote_addr
    save_ip_hit(ip, request.url_rule.rule)
    return jsonify({'message': 'hello world'})

@app.route('/v1/logs')
@app.route('/v1/<path:path>/logs')
@requires_auth
def logs(path=False):
    if not path:
        path = '*'

    match = 'ip:*path:/v1/{}'.format(path)

    matched_logs = []
    for key in cache.scan_iter(match=match):
        matched_logs += [{'ip': key.decode('utf-8').split('path:')[0].split('ip:')[1], 'timestamp':stamp.decode('utf-8')}
                         for stamp in cache.lrange(key, 0, -1)]

    return jsonify({'logs':matched_logs})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)