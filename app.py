from flask import Flask, jsonify, request
import traceback
app = Flask(__name__)

#404 handler
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Your requested url could not be found' +request.url,
    }
    res = jsonify(message)
    res.status_code = 404
    return res

#403 handler
@app.errorhandler(403)
def forbidden(error=None):
    message = {
        'status': 403,
        'message': 'Forbidden'
    }
    res = jsonify(message)
    res.status_code = 403
    return res

# 500 handler
@app.errorhandler(500)
def internal_server_error(error=None):
    message = {
        'status': 500,
        'message': 'Failed to process request',
    }
    res = jsonify(message)
    res.status_code = 500
    traceback.print_exc()
    return res

#CORS section
@app.after_request
def after_request_func(response):
    response.headers.add('Access-Control-Allow-Origin',"*")
    response.headers.add('Access-Control-Allow-Headers',"*")
    response.headers.add('Access-Control-Allow-Methods',"*")
    return response

#endpoints
from routes import login
from routes import register
from routes import dashboard

@app.route('/')
def get_endpoint_function():
    try:
        res = "<h1 style='position: fixed; top: 50%;  left: 50%; transform: translate(-50%, -50%);'>DENX API</h1>"
        return res
    except Exception as e:
        print(e)

if __name__ == "main":
    app.run(debug=True)