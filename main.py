from flask import Flask, request, jsonify
import os
import json
from tasks import execute_task

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run():
    """Executes a task based on the description"""
    task_description = request.args.get('task')
    
    if not task_description:
        return jsonify({"error": "No task description provided"}), 400

    try:
        result = execute_task(task_description)
        return jsonify({"message": "Task executed successfully", "result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs("/data", exist_ok=True)  # Ensure data directory exists
    app.run(debug=True, host='0.0.0.0', port=8000)
