import time
import json
import random
import paho.mqtt.client as mqtt

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    
MQTT_BROKER = config["mqtt"]["broker"]
MQTT_PORT = config["mqtt"]["port"]
PARAMETERS = config["parameters"]
HOUSES = config["houses"]

# State dictionary to store the last known values for each sensor
sensor_states = {
    "temperature": 20.0,  # Starting point for temperature
    "humidity": 90.0,     # Starting point for humidity
    "co2": 600.0          # Starting point for CO2
}

# Simulate realistic gradual changes for a given sensor
def simulate_gradual_change(sensor_type):
    if sensor_type == "temperature":
        # Adjust temperature by ±0.5°C
        change = random.uniform(-0.5, 0.5)
        sensor_states[sensor_type] = max(10, min(25, sensor_states[sensor_type] + change))
    elif sensor_type == "humidity":
        # Adjust humidity by ±1%
        change = random.uniform(-1, 1)
        sensor_states[sensor_type] = max(85, min(95, sensor_states[sensor_type] + change))
    elif sensor_type == "co2":
        # Adjust CO2 by ±10 ppm
        change = random.uniform(-10, 10)
        sensor_states[sensor_type] = max(400, min(800, sensor_states[sensor_type] + change))
    
    return round(sensor_states[sensor_type], 2)

# Generate abnormal data within the given range (supports both too low & too high)
def generate_abnormal_data(sensor_type):
    abnormal_range = PARAMETERS[sensor_type]["abnormal_range"]

    if isinstance(abnormal_range[0], list):  # If abnormal range has both low and high values
        low_range = abnormal_range[0]
        high_range = abnormal_range[1]
        
        if random.random() < 0.5:  # 50% chance to pick low or high abnormal value
            return round(random.uniform(low_range[0], low_range[1]), 2)
        else:
            return round(random.uniform(high_range[0], high_range[1]), 2)

    return round(random.uniform(abnormal_range[0], abnormal_range[1]), 2)

# Generate data with occasional abnormalities
def get_data(sensor_type):
    if random.random() < 0.05:  # 5% chance for abnormal data
        return generate_abnormal_data(sensor_type)
    else:
        return simulate_gradual_change(sensor_type)

# MQTT Connection Callback
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT broker!")
    else:
        print(f"Failed to connect, reason code: {reason_code}")

# Wait for the MQTT broker to become available
def wait_for_broker(client, host, port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            client.connect(host, port, keepalive=60)
            print("Successfully connected to MQTT broker.")
            return
        except ConnectionRefusedError:
            print("Waiting for MQTT broker...")
            time.sleep(1)
    raise Exception("Could not connect to MQTT broker within timeout period.")

# MQTT Publisher
def publish_data():
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.on_connect = on_connect

    wait_for_broker(client, MQTT_BROKER, MQTT_PORT)

    client.loop_start()

    try:
        while True:
            for house_name, house_data in HOUSES.items():
                for sensor_name, sensor_info in house_data["sensors"].items():
                    sensor_type = sensor_name.split("_")[0]  # Extract sensor type (temperature, humidity, co2)
                    value = get_data(sensor_type)
                    client.publish(sensor_info["topic"], value)
                    print(f"[{house_name}] Published: {sensor_name} = {value} to {sensor_info['topic']}")

            time.sleep(10)  # Publish every 10 seconds

    except KeyboardInterrupt:
        print("\nStopping MQTT publisher...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    publish_data()