from flask import Flask, jsonify, render_template  # render_template 추가
import serial
import time
import threading

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

app = Flask(__name__)

data = {"humidity": 0.0, "temperature": 0.0, "weight": 0.0}

def read_from_arduino():
    global data
    while True:
        if ser.in_waiting > 0:  # 오타 수정: in_wating -> in_waiting
            line = ser.readline().decode('utf-8').rstrip()
            if "Temperature" in line and "Humidity" in line:
                parts = line.split(",")
                temp_part = parts[0].split(":")[1]
                hum_part = parts[1].split(":")[1]
                data["temperature"] = float(temp_part.replace("C", ""))
                data["humidity"] = float(hum_part.replace("%", ""))  # 오타 수정: temp_part -> hum_part
            elif "Weight" in line:
                weight_part = line.split(": ")[1]
                data["weight"] = float(weight_part.replace(" kg", ""))
        time.sleep(1)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # render_template에 data 전달

@app.route('/data', methods=['GET', 'POST'])
def get_data():
    return jsonify(data)

if __name__ == "__main__":
    threading.Thread(target=read_from_arduino).start()
    app.run(host="172.30.1.29", port="8080", debug=True)
