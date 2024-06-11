#include <DHT.h>
#include "HX711.h"
#define DHTPIN A0
#define DHTTYPE DHT11 

// RGB LED 핀 설정
int redPin = 9;
int greenPin = 10;
int bluePin = 13;

#define calibration_factor -7050.0 // 로드 셀의 교정 값 (lbs 단위)
#define conversion_factor 0.453592 // lbs를 kg으로 변환하는 계수

#define DOUT 3 // 로드 셀 데이터 출력 핀 (DT)
#define CLK 2 // 로드 셀 클럭 핀 (SCK)

HX711 scale(DOUT, CLK); // 로드 셀 핀 선언

DHT dht(DHTPIN, DHTTYPE);

int sensor = 7; // PIR 센서 입력 핀
int value = 0; // PIR 센서 값을 저장할 변수

void setup() {
  Serial.begin(9600); 
  dht.begin(); 
  pinMode(sensor, INPUT); // 센서 핀을 입력으로 설정

  // LED 핀을 출력으로 설정
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  // 로드 셀 초기화
  scale.set_scale(calibration_factor / conversion_factor);
  scale.tare(); // 로드 셀 초기화
  Serial.println("Readings: ");
}

void loop() {
  // 시리얼 입력 확인
  if (Serial.available()) {
    char command = Serial.read();
    if (command == '1') {
      setColor(255, 0, 0); // LED를 빨간색으로 켜기
    } else if (command == '0') {
      setColor(0, 0, 0); // LED 끄기
    }
  }

  // 무게 센서 출력
  Serial.print("Weight: ");
  Serial.print(scale.get_units(), 1); // 무게 출력
  Serial.println(" kg");

  // 온도와 습도 출력
  int h = dht.readHumidity();
  int t = dht.readTemperature();
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print("C, Humidity: ");
  Serial.print(h);
  Serial.println("%");

  // PIR 센서 출력
  value = digitalRead(sensor); // PIR 센서 값 읽기
  if (value == HIGH) {
    Serial.println("움직임이 감지되었습니다."); // 움직임이 감지되었을 때 출력
  } else {
    Serial.println("움직임 x."); // 움직임이 감지되지 않았을 때 출력
  }

  delay(2000); // 다음 루프 전 2초 대기
}

// RGB LED 색상 설정 함수
void setColor(int red, int green, int blue) {
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue); 
}
