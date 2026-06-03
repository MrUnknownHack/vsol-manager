from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from speed_monitor import get_all_onu_speeds
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Simple in-memory storage for history (will reset on deploy)
# For production, use PostgreSQL
speed_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/speeds')
def get_speeds():
    speeds = get_all_onu_speeds()
    
    # Save to history
    timestamp = datetime.now().isoformat()
    for onu in speeds:
        speed_history.append({
            "timestamp": timestamp,
            "onu_id": onu["onu_id"],
            "rx_speed": onu["rx_speed"],
            "tx_speed": onu["tx_speed"]
        })
    
    # Keep only last 1000 records
    while len(speed_history) > 1000:
        speed_history.pop(0)
    
    return jsonify(speeds)

@app.route('/api/history')
def get_history():
    """Get historical speed data for graphs"""
    onu_id = request.args.get('onu_id', '1')
    
    filtered = [h for h in speed_history if h["onu_id"] == onu_id]
    
    # Return last 50 records
    return jsonify(filtered[-50:])

@app.route('/api/users')
def get_users():
    """Get user mapping"""
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
        return jsonify(users)
    except:
        return jsonify({})

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)