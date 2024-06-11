import serial
import time

def main():
    port = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    time.sleep(2)  # 포트 안정화를 위한 대기 시간 추가

    while True:
        line = port.readline()
        try:
            line = line.decode('utf-8', errors='ignore').strip()
        except UnicodeDecodeError:
            continue

        if not line:
            continue

        arr = line.split()
        if len(arr) < 3:
            continue
        
        try:
            data = float(arr[1])  # 값 저장 
            dataType = arr[2]  # 데이터 타입 (%, C, kg)

            if dataType == '%':
                print("humidity= %.1f %%" % data)
            elif dataType == 'C': 
                print("temperature= %.1f C" % data)
            elif dataType == 'kg':
                print("weight= %.1f kg" % data)
        
        except ValueError:
            continue
        
        time.sleep(0.1)    

if __name__ == "__main__":
    main()
