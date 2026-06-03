from flask import Flask, jsonify, render_template
from flask_cors import CORS
from speed_monitor import get_all_onu_speeds

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/speeds')
def get_speeds():
    speeds = get_all_onu_speeds()
    return jsonify(speeds)

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)