#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

String message;
String message2;
int lcdColumns = 16;
int lcdRows = 2;

// Declaration for an LCD display connected via I2C
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows); // I2C address may vary, adjust accordingly

const char* ssid = "SSID";
const char* password = "PASS";
const char* APIAddress = "IP";
const char* User = "IQ";
int flowPin = 18;
volatile long pulse = 0;
float previous = 0;

void IRAM_ATTR increase(); // Function prototype

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Connected to WiFi");

  pinMode(flowPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(flowPin), increase, RISING);

  lcd.init();
  lcd.backlight();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    unsigned int pulse = pulseIn(flowPin, HIGH);
    pulse++; // Increment pulse count
    float pltoml = pulse * 2.25; // Convert to mL
    float mltocm3 = pltoml / 1000; // Convert to cm3
    float unit = mltocm3 / 1000; // Convert to m3 or unit

    message = "pltoml  = ";
    message2 = String(pltoml) + " mL ";

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(message);
    lcd.setCursor(0, 1);
    lcd.print(message2);

    Serial.println(message2);
    Serial.println();

    if (previous != unit) {
      HTTPClient http;
      WiFiClient client;
      http.begin(client, APIAddress);

      http.addHeader("Content-Type", "application/json");
      String lit2unitStr = String(unit, 2);
      String payload = "{\"Update\": true, \"Username\": \""+ User +"\", \"Unit\": \"" + lit2unitStr + "\"}";

      int httpResponseCode = http.POST(payload);

      if (httpResponseCode == HTTP_CODE_OK) {
        String response = http.getString();
        Serial.println("Request sent successfully");
        Serial.println("Response: " + response);
      } else {
        Serial.print("Error sending HTTP request. Error code: ");
        Serial.println(httpResponseCode);
      }

      previous = unit;
      http.end();
    }
  }

  delay(5000);
}

void IRAM_ATTR increase() {
  // Empty ISR since pulse count is now obtained using pulseIn() function
}
