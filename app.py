from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Data file path
DATA_FILE = 'attendance_data.json'

def load_attendance_data():
    """Load attendance data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_attendance_data(data):
    """Save attendance data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """Get all attendance records"""
    data = load_attendance_data()
    return jsonify(data)

@app.route('/api/attendance', methods=['POST'])
def add_attendance():
    """Add a new attendance record"""
    req_data = request.json
    data = load_attendance_data()
    
    if 'name' not in req_data:
        return jsonify({'error': 'Name is required'}), 400
    
    name = req_data['name']
    status = req_data.get('status', 'Present')
    date = req_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    if name not in data:
        data[name] = []
    
    # Check if record already exists for this date
    for record in data[name]:
        if record['date'] == date:
            record['status'] = status
            save_attendance_data(data)
            return jsonify({'message': 'Attendance updated'}), 200
    
    data[name].append({'date': date, 'status': status})
    save_attendance_data(data)
    return jsonify({'message': 'Attendance added'}), 201

@app.route('/api/attendance/<name>', methods=['GET'])
def get_person_attendance(name):
    """Get attendance records for a specific person"""
    data = load_attendance_data()
    if name in data:
        return jsonify({name: data[name]})
    return jsonify({'error': 'Person not found'}), 404

@app.route('/api/attendance/<name>', methods=['DELETE'])
def delete_person(name):
    """Delete a person's attendance records"""
    data = load_attendance_data()
    if name in data:
        del data[name]
        save_attendance_data(data)
        return jsonify({'message': 'Person deleted'}), 200
    return jsonify({'error': 'Person not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)