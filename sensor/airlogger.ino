#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#define SDA_PIN 4
#define SCL_PIN 5

#define NEO_PIN 38
#define NEO_NUM 2
#define WIFI_LED_PIN 13

String location = "A013";
String api_key = "36!fs@s63gc%";

const char *ssid = "<NETWORK-NAME>";
const char *password = "<NETWORK-PASSWORD>";
const char *api = "http://ikj023.csano.no/api/sensors/submit-bme680-sensor-data";

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NEO_NUM, NEO_PIN, NEO_GRB + NEO_KHZ800);

Adafruit_BME680 sensor;

void setup() {

  // Config. hardware.
  Serial.begin(9600);
  while (!Serial);
  Wire.begin(SDA_PIN, SCL_PIN);
  pinMode(WIFI_LED_PIN, OUTPUT);
  digitalWrite(WIFI_LED_PIN, LOW);
  pixels.begin();
  pixels.show();
  pixels.setBrightness(64);

  // Init. BME680 sensor.
  if (!sensor.begin(0x76)) {
    pixels.setPixelColor(0, pixels.Color(255, 0, 0));
    pixels.setPixelColor(1, pixels.Color(255, 0, 0));
    pixels.show();
    while(1);
  }

  // Apply BME680 filters and settings.
  sensor.setTemperatureOversampling(BME680_OS_8X);
  sensor.setHumidityOversampling(BME680_OS_2X);
  sensor.setPressureOversampling(BME680_OS_4X);
  sensor.setIIRFilterSize(BME680_FILTER_SIZE_3);
  sensor.setGasHeater(320, 150);

  // Connect to WiFi.
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  digitalWrite(WIFI_LED_PIN, HIGH);
}

unsigned long ms_timer = 0;
unsigned long ms_delay = 10000;

void loop() {

  // Indicate running program.
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(WIFI_LED_PIN, HIGH);
    delay(500);
    digitalWrite(WIFI_LED_PIN, LOW);
    delay(500);
    digitalWrite(WIFI_LED_PIN, HIGH);
  } else {
    digitalWrite(WIFI_LED_PIN, LOW);
    pixels.setPixelColor(0, pixels.Color(0, 0, 255));
    pixels.setPixelColor(1, pixels.Color(0, 0, 255));
  }

  // Send data to server after a given delay.
  if ((millis() - ms_timer) > ms_delay) {

    // Read data from the sensor.
    if (!sensor.performReading()) {
      pixels.setPixelColor(0, pixels.Color(255, 0, 0));
    } else {
      pixels.setPixelColor(0, pixels.Color(0, 255, 0));
    }

    if (WiFi.status() == WL_CONNECTED) {
      digitalWrite(WIFI_LED_PIN, HIGH);

      WiFiClient client;
      HTTPClient http;

      client.setTimeout(5000);
      http.begin(client, api);

      String temperature = String(sensor.temperature);
      String pressure = String(sensor.pressure);
      String humidity = String(sensor.humidity);
      String gas_resistance = String(sensor.gas_resistance);

      String raw_json_data = "{\"api_key\":\"" + api_key + "\",\"location\":\"" + location + "\",\"temperature\":\"" + temperature + "\",\"pressure\":\"" + pressure + "\",\"humidity\":\"" + humidity + "\",\"gas_resistance\":\"" + gas_resistance + "\"}";

      Serial.println(raw_json_data);

      // POST JSON data containing raw sensor data.
      http.addHeader("Content-Type", "application/json");
      if (http.POST(raw_json_data) == 201) {
        pixels.setPixelColor(1, pixels.Color(0, 255, 0));
      } else {
        pixels.setPixelColor(1, pixels.Color(255, 0, 0));
      }

      http.end();

    } else {
      digitalWrite(WIFI_LED_PIN, LOW);
    }

    ms_timer = millis();
    pixels.show();
  }
}
