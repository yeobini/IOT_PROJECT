import serial
import time
from flask import Flask, render_template_string

ser=serial.Serial("/dev/ttyACM0",9600)

app = Flask(__name__)

def read_sensor_data():
    data = {'humidity': 0.0, 'temperature': 0.0, 'weight': 0.0}
    try:
        with open('sensor_data.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('humidity='):
                    data['humidity'] = float(line.split('=')[1].strip())
                elif line.startswith('temperature='):
                    data['temperature'] = float(line.split('=')[1].strip())
                elif line.startswith('weight='):
                    data['weight'] = float(line.split('=')[1].strip())
    except FileNotFoundError:
        pass
    return data

@app.route('/')
def hello():
    sensor_data = read_sensor_data()
    return render_template_string("""
    <html>
      <head>
        <title>Sensor Data Display</title>
      </head>
      <body>
        <h1>Sensor Data</h1>
        <p>Humidity: {{ humidity }} %</p>
        <p>Temperature: {{ temperature }} °C</p>
        <p>Weight: {{ weight }} kg</p>
        <h1>LED Control</h1>
        <button onclick="window.location.href='/led_on'">Turn LED On</button>
        <button onclick="window.location.href='/led_off'">Turn LED Off</button>
      </body>
    </html>
    """, humidity=sensor_data['humidity'], temperature=sensor_data['temperature'], weight=sensor_data['weight'])

@app.route('/led_on')       # IP주소:port/red_on 을 입력하면 나오는 페이지
def led_on():               # 해당 페이지의 뷰함수 정의
   ser.write(b'1')  # 빨간 LED 핀에 HIGH 신호 인가(LED 켜짐)
   return "led LED on"              # 뷰함수의 리턴값

@app.route('/led_off')     # IP주소:port/green_on 을 입력하면 나오는 페이지
def led_off():             # 해당 페이지의 뷰함수 정의
   ser.write(b'0') # 초록 LED 핀에 HIGH 신호 인가(LED 켜짐)
   return "led LED off"    

if __name__ == "__main__":
    app.run(host="172.30.1.29", port = "8080",debug=True)
