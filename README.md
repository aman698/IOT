# IOT
ESP32 Code (Publisher)
Use the Arduino IDE to program the ESP32. You need the DHT and PubSubClient libraries and file is main.cpp

Raspberry Pi 4 Code (Subscriber)
This code subscribes to the MQTT topic, checks if the temperature crosses a threshold, and saves the data locally. It also runs the HTTP server and file is main.py
