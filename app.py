from flask import Flask, jsonify, render_template
from flask_cors import CORS
from speed_monitor import get_all_onu_speeds
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/speeds')
def api_speeds():
    speeds = get_all_onu_speeds()
    return jsonify(speeds)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)