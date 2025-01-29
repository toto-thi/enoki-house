import random
import time
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = "mosquitto"  
MQTT_PORT = 1883
MQTT_TOPIC_TEMPERATURE = "enoki/temperature"
MQTT_TOPIC_HUMIDITY = "enoki/humidity"
MQTT_TOPIC_CO2 = "enoki/co2"

# Generate normal data within realistic ranges
def generate_data(sensor):
    if sensor == "Temperature (°C)":
        return round(random.uniform(10, 25), 2)  # Normal temperature range
    elif sensor == "Humidity (%)":
        return round(random.uniform(85, 95), 2)  # Normal humidity range
    elif sensor == "CO2 (ppm)":
        return round(random.uniform(400, 800), 2)  # Normal CO2 range

# Generate abnormal data for specific sensors
def generate_abnormal_data(sensor):
    if sensor == "Temperature (°C)":
        return round(random.uniform(0, 9), 2)  # Abnormally low temperature
    elif sensor == "Humidity (%)":
        return round(random.uniform(75, 84), 2)  # Abnormally low humidity
    elif sensor == "CO2 (ppm)":
        return round(random.uniform(1001, 1500), 2)  # Abnormally high CO2 levels

# Generate data with occasional abnormalities
def get_data(sensor):
    if random.random() < 0.05:  # 5% chance for abnormal data
        return generate_abnormal_data(sensor)
    else:
        return generate_data(sensor)
    
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
        sensors = ["Temperature (°C)", "Humidity (%)", "CO2 (ppm)"]
        while True:
            for sensor in sensors:
                value = get_data(sensor)
                if sensor == "Temperature (°C)":
                    client.publish(MQTT_TOPIC_TEMPERATURE, value)
                elif sensor == "Humidity (%)":
                    client.publish(MQTT_TOPIC_HUMIDITY, value)
                elif sensor == "CO2 (ppm)":
                    client.publish(MQTT_TOPIC_CO2, value)

                print(f"Published: {sensor} = {value}")
            time.sleep(10)  # Publish every 10 seconds

    except KeyboardInterrupt:
        print("\nStopping MQTT publisher...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    publish_data()