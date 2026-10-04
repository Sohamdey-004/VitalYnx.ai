// PulseGuard AI Wokwi demo: simulated data only, not a medical device.
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <HTTPClient.h>
Adafruit_SSD1306 display(128,64,&Wire,-1);
const int GREEN=25,YELLOW=26,RED=27,BUZZER=14;
const char* WIFI_SSID="Wokwi-GUEST"; const char* WIFI_PASSWORD="";
const char* SERVER_URL="http://YOUR_SERVER/api/reading"; const char* API_KEY="set-in-your-deployment";
String mode="NORMAL";
unsigned long lastReadingAt=0;
const unsigned long READING_INTERVAL=10000;
void show(String line){display.clearDisplay();display.setTextSize(1);display.setTextColor(WHITE);display.setCursor(0,0);display.println("PULSEGUARD AI");display.println("SIMULATED DEMO");display.println(line);display.display();}
void statusLights(String m){digitalWrite(GREEN,m=="NORMAL");digitalWrite(YELLOW,m=="TACHYCARDIA"||m=="LOW_SPO2"||m=="HIGH_BP");digitalWrite(RED,m=="ABNORMAL"||m=="EMERGENCY");if(m=="EMERGENCY") tone(BUZZER,1100,250);}
void sendReading(int p,int o,int s,int d){if(WiFi.status()!=WL_CONNECTED)return;HTTPClient http;http.begin(SERVER_URL);http.addHeader("Content-Type","application/json");http.addHeader("X-ESP32-API-Key",API_KEY);String body="{\"user_id\":1,\"pulse\":"+String(p)+",\"spo2\":"+String(o)+",\"systolic\":"+String(s)+",\"diastolic\":"+String(d)+",\"heart_rate\":"+String(p)+",\"ecg\":[0.0,0.1,0.8,-0.2],\"signal_quality\":\"simulated\"}";http.POST(body);http.end();}
void runMode(){int p=78,o=98,s=120,d=78;if(mode=="TACHYCARDIA"){p=122;s=130;d=84;}if(mode=="LOW_SPO2"){p=92;o=91;}if(mode=="HIGH_BP"){s=158;d=98;}if(mode=="ABNORMAL"){p=128;o=92;s=165;d=104;}if(mode=="EMERGENCY"){p=142;o=87;s=186;d=122;}statusLights(mode);show(mode+"\nP "+String(p)+" O2 "+String(o)+"\nBP "+String(s)+"/"+String(d));sendReading(p,o,s,d);}
void setup(){Serial.begin(115200);pinMode(GREEN,OUTPUT);pinMode(YELLOW,OUTPUT);pinMode(RED,OUTPUT);display.begin(SSD1306_SWITCHCAPVCC,0x3C);WiFi.begin(WIFI_SSID,WIFI_PASSWORD);show("WiFi connecting...");while(WiFi.status()!=WL_CONNECTED&&millis()<10000)delay(200);runMode();lastReadingAt=millis();Serial.println("Commands: NORMAL TACHYCARDIA LOW_SPO2 HIGH_BP ABNORMAL EMERGENCY");}
void loop(){if(Serial.available()){mode=Serial.readStringUntil('\n');mode.trim();mode.toUpperCase();runMode();lastReadingAt=millis();}if(millis()-lastReadingAt>=READING_INTERVAL){runMode();lastReadingAt=millis();}delay(100);}
