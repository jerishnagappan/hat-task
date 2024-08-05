
from flask import Flask, jsonify, request
from honeybadger.contrib import FlaskHoneybadger

app = Flask(__name__)
app.config['HONEYBADGER_ENVIRONMENT'] = 'production'
app.config['HONEYBADGER_API_KEY'] = 'hbp_C34un88dv5j8VPswh8uJywoH7yBsXB4AoiKz'
app.config['HONEYBADGER_PARAMS_FILTERS'] = ['password', 'secret', 'credit-card']


honeybadger = FlaskHoneybadger(app, report_exceptions=True)

@app.route('/')
def index():
    try:
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))

        print(f"Received values: a = {a}, b = {b}")
        result = a / b
        print(f"Division result: {result}")

        return jsonify({'result': result})
    except Exception as e:
        
        honeybadger.notify(e)
        print(f"Error reported to Honeybadger: {e}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/test-connection', methods=['GET'])
def test_connection():

    try:
        
        raise ValueError("Testing Honeybadger connection")
    except Exception as e:
        honeybadger.notify(e)
        return jsonify({'message': 'Connection test error reported to Honeybadger'}), 200

if __name__ == "__main__":
    app.run(debug=True)
