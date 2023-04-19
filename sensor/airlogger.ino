#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

// Hardware layout.
#define SDA_PIN 4
#define SCL_PIN 5
#define NEO_PIN 38
#define NEO_NUM 2
#define WIFI_LED_PIN 13

// POST data with a given delay.
unsigned long ms_delay = 60000;

// Sensor settings.
const char *ssid = "<NETWORK-NAME>";
const char *password = "<NETWORK-PASSWORD>";
const char *api = "<API-PATH>";
String api_key = "<API-KEY>";
String location = "<LOCATION>";

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
}

unsigned long ms_timer = 0;

void loop() {

    // Indicate running program.
    if (WiFi.status() == WL_CONNECTED) {
        digitalWrite(WIFI_LED_PIN, HIGH);
        delay(100);
        digitalWrite(WIFI_LED_PIN, LOW);
        delay(100);
        digitalWrite(WIFI_LED_PIN, HIGH);
    } else {
        // Indicate loss of WiFi.
        digitalWrite(WIFI_LED_PIN, LOW);
        pixels.setPixelColor(0, pixels.Color(0, 0, 255));
        pixels.setPixelColor(1, pixels.Color(0, 0, 255));
    }

    // Send data to server after a given delay.
    if ((millis() - ms_timer) > ms_delay) {

        // Read data from the sensor.
        if (!sensor.performReading()) {
            // Indicate broken sensor.
            pixels.setPixelColor(0, pixels.Color(255, 0, 0));
        } else {
            // Indicate working sensor.
            pixels.setPixelColor(0, pixels.Color(0, 255, 0));
        }

        // Only attempt POST with a valid network connection.
        if (WiFi.status() == WL_CONNECTED) {

            WiFiClient client;
            HTTPClient http;

            client.setTimeout(5000);
            http.begin(client, api);

            // Convert float values to strings.
            String temperature = String(sensor.temperature);
            String pressure = String(sensor.pressure);
            String humidity = String(sensor.humidity);
            String gas_resistance = String(sensor.gas_resistance);

            // Create the JSON object.
            String json_data = "{
                \"api_key\":\"" + api_key + "\",
                \"location\":\"" + location + "\",
                \"temperature\":\"" + temperature + "\",
                \"pressure\":\"" + pressure + "\",
                \"humidity\":\"" + humidity + "\",
                \"tvoc\":\"" + tvoc + "\"
            }";

            // Output JSON to the terminal.
            Serial.println(json_data);

            // POST JSON data containing the sensor values.
            http.addHeader("Content-Type", "application/json");
            if (http.POST(json_data) == 201) {
                // Indicate successful POST.
                pixels.setPixelColor(1, pixels.Color(0, 255, 0));
            } else {
                // Indicate failed POST.
                pixels.setPixelColor(1, pixels.Color(255, 0, 0));
            }

            http.end();
        }

        ms_timer = millis();
    }

    pixels.show();
}
