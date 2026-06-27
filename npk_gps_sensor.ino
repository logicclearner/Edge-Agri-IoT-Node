#include <SoftwareSerial.h>
#include <TinyGPS++.h>

// --- PIN DEFINITIONS ---
#define RE_PIN 6
#define DE_PIN 7

SoftwareSerial npkSerial(10, 11);
SoftwareSerial gpsSerial(8, 9);
TinyGPSPlus gps;

byte response[11];
byte command[] = {0x01, 0x03, 0x00, 0x1E, 0x00, 0x03, 0x00, 0x00};

uint16_t modRTU_CRC(byte buf[], int len) {
  uint16_t crc = 0xFFFF;
  for (int pos = 0; pos < len; pos++) {
    crc ^= (uint16_t)buf[pos];
    for (int i = 8; i != 0; i--) {
      if ((crc & 0x0001) != 0) {
        crc >>= 1;
        crc ^= 0xA001;
      } else {
        crc >>= 1;
      }
    }
  }
  return crc;
}

void setup() {
  Serial.begin(9600);
  npkSerial.begin(9600);
  gpsSerial.begin(9600);
  pinMode(RE_PIN, OUTPUT);
  pinMode(DE_PIN, OUTPUT);
  digitalWrite(RE_PIN, LOW);
  digitalWrite(DE_PIN, LOW);
  
  // CSV HEADER
  Serial.println("Date, Time, Latitude, Longitude, Nitrogen_N,Phosphorus_P,Potassium_K");
}

void loop() {
  // 1. GPS COLLECTION (Reduced to 1 second)
  gpsSerial.listen();
  unsigned long gpsStart = millis();
  while (millis() - gpsStart < 1000) {
    while (gpsSerial.available() > 0) {
      gps.encode(gpsSerial.read());
    }
  }

  // 2. NPK COLLECTION
  npkSerial.listen();
  uint16_t crc = modRTU_CRC(command, 6);
  command[6] = lowByte(crc);
  command[7] = highByte(crc);
  
  while (npkSerial.available()) npkSerial.read();
  
  digitalWrite(RE_PIN, HIGH);
  digitalWrite(DE_PIN, HIGH);
  delay(10);
  npkSerial.write(command, 8);
  npkSerial.flush();
  digitalWrite(RE_PIN, LOW);
  digitalWrite(DE_PIN, LOW);
  
  unsigned long start = millis();
  bool frameStarted = false;
  
  // Reduced timeout for sensor response
  while (millis() - start < 500) {
    if (npkSerial.available() > 0) {
      if (npkSerial.peek() == 0x01) {
        frameStarted = true;
        break;
      } else {
        npkSerial.read();
      }
    }
  }

  if (frameStarted) {
    unsigned long waitFull = millis();
    while(npkSerial.available() < 11 && millis() - waitFull < 200);
    if (npkSerial.available() >= 11) {
      for (int i = 0; i < 11; i++) response[i] = npkSerial.read();
      uint16_t receivedCRC = (response[10] << 8) | response[9];
      uint16_t calculatedCRC = modRTU_CRC(response, 9);
      if (receivedCRC == calculatedCRC) {
        int N = (response[3] << 8) | response[4];
        int P = (response[5] << 8) | response[6];
        int K = (response[7] << 8) | response[8];
        // Output CSV Line
        printCSVLine(N, P, K);
      }
    }
  }
  delay(500);
}

void printCSVLine(int n, int p, int k) {
  // Date
  if (gps.date.isValid()) {
    Serial.print(gps.date.day()); Serial.print("/");
    Serial.print(gps.date.month()); Serial.print("/");
    Serial.print(gps.date.year());
  }
  Serial.print(",");
  
  // Time
  if (gps.time.isValid()) {
    if (gps.time.hour() < 10) Serial.print("0"); 
    Serial.print(gps.time.hour());
    Serial.print(":");
    if (gps.time.minute() < 10) Serial.print("0"); 
    Serial.print(gps.time.minute());
    Serial.print(":");
    if (gps.time.second() < 10) Serial.print("0"); 
    Serial.print(gps.time.second());
  }
  Serial.print(",");
  
  // Lat/Lng
  if (gps.location.isValid()) {
    Serial.print(gps.location.lat(), 6); Serial.print(",");
    Serial.print(gps.location.lng(), 6); Serial.print(",");
  } else {
    Serial.print("0,0,");
  }
  
  // NPK
  Serial.print(n); Serial.print(",");
  Serial.print(p); Serial.print(",");
  Serial.println(k);
}
