#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

const char* ssid = "AMAN LAKRA";
const char* password = "Aman@124";

const char* mqtt_server = "192.168.1.59";
const char* mqtt_topic = "sensor/temperature";

WiFiClient espClient;
PubSubClient client(espClient);

#define DHTPIN 4 
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float temperature = dht.readTemperature();
  
  if (isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  char tempStr[8];
  dtostrf(temperature, 1, 2, tempStr);
  client.publish(mqtt_topic, tempStr);
  Serial.print("Published: ");
  Serial.println(tempStr);

  delay(60000); 
}
