# Enoki Mushroom Cultivation House 🌱🍄

Automating Enoki mushroom growth with an IoT-based climate control system.

Growing Enoki mushrooms (Flammulina velutipes) requires strict environmental control, including low `temperatures`, `high humidity`, and precise `CO₂` levels. Traditional cultivation methods often rely on manual adjustments, which can lead to inconsistent growth conditions, inefficient resource usage, and increased labor costs.

We propose an IoT-based automated cultivation system to streamline mushroom farming operations. By integrating real-time environmental monitoring and automated climate control, this system ensures optimal growing conditions with minimal manual intervention.

To demonstrate this approach, we simulate a controlled Enoki mushroom growing environment, where `temperature, humidity, and CO₂` sensors continuously feed data into an automation system built with `Node-RED`, `MQTT`, and `Python-based` simulations. The system automatically regulates humidifiers, ventilation, and temperature control devices based on sensor readings. Additionally, data is stored in `InfluxDB` and visualized in `Grafana`, allowing for real-time monitoring and historical analysis.

## Built with

| Technology       |                                                           Logo                              | Description                                  |
|-------------------|---------------------------------------------------------------------------------------------|----------------------------------------------|
| Docker           | ![Docker](https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png)                  | A platform for containerization, allowing us to package and deploy applications efficiently. Each component (Node-RED, InfluxDB, Grafana, and Mosquitto) runs in an isolated container, ensuring flexibility, scalability, and simplified maintenance.  |
| Apache Mosquitto | ![Apache Mosquitto](https://vmssoftware.com/images/intro/product/mosquitto.png) | A lightweight MQTT broker that facilitates real-time communication between sensors, actuators, and the control system. It enables efficient data exchange with minimal network bandwidth.        |
| Node-RED         | ![Node-RED](https://upload.wikimedia.org/wikipedia/commons/2/2b/Node-red-icon.png)          | A flow-based development tool used for wiring together devices, APIs, and services in a visual interface. It acts as the control system, processing sensor data and automating environmental adjustments based on predefined conditions.          |
| InfluxDB         | ![InfluxDB](https://marketplace.thinger.io/plugins/influxdb2/assets/influxdb.svg)           | A time-series database optimized for handling sensor data. It stores historical records of temperature, humidity, and CO₂ levels, allowing for long-term analysis and performance tracking.            |
| Grafana          | ![Grafana](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Grafana_logo.svg/800px-Grafana_logo.svg.png) | A powerful analytics and visualization tool. It connects to InfluxDB and provides real-time monitoring dashboards, historical data insights, and customizable alerts to track environmental changes effectively.  |

## Data Flow

![Data Flow]('/images/data-flow.png')

## Getting Start

Note: Your machine must have docker installed before testing our simulation.

You can start playing with this project by simply run this command:

```bash
docker compose up --build -d
```

Then you can open your web browser and access the following services:

To view Node-RED Flow visit: **[localhost:1880](http://localhost:1880)**

To view InfluxDB Database visit: **[localhost:8086](http://localhost:8086)**

```bash
Username: admin
Password: admin123
```

To view Grafana Dashboard visit: **[localhost:3000](http://localhost:3000)**

```bash
Username: admin
Password: admin777#
```

To receive notification of our actuator actions, please interact with our **[Enoki-bot](https://t.me/EnokiiBot)** on Telegram.
