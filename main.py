import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime
from flask import Flask, jsonify

MQTT_BROKER = "192.168.1.59"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperature"
THRESHOLD = 30 
ALARM_DURATION = 5  

temp_data = []
alarm_active = False

def save_data(data):
    with open("sensor_data.json", "a") as file:
        file.write(json.dumps(data) + "\n")

def check_threshold():
    global alarm_active
    if len(temp_data) >= ALARM_DURATION:
        last_five_readings = [data['temperature'] for data in temp_data[-ALARM_DURATION:]]
        if all(temp >= THRESHOLD for temp in last_five_readings):
            if not alarm_active:
                print("Alarm: Temperature threshold crossed for 5 minutes")
                alarm_active = True
        else:
            alarm_active = False

def on_message(client, userdata, msg):
    temperature = float(msg.payload.decode())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"timestamp": timestamp, "temperature": temperature}
    temp_data.append(data)
    save_data(data)
    check_threshold()
    print(f"Received: {temperature} at {timestamp}")

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()

app = Flask(__name__)

def get_last_sensor_value():
    try:
        with open("sensor_data.json", "r") as file:
            lines = file.readlines()
            if lines:
                return json.loads(lines[-1])
            else:
                return None
    except FileNotFoundError:
        return None

@app.route('/sensor_data', methods=['GET'])
def sensor_data():
    data = get_last_sensor_value()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "No data available"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
