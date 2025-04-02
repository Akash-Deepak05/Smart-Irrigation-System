# Smart Irrigation System

## Overview
The Smart Irrigation System is an IoT-based project designed to automate irrigation by monitoring soil moisture, temperature, humidity, and water level. The system uses an ESP32 microcontroller along with various sensors and modules to ensure optimal watering of plants. It integrates with Blynk for remote monitoring and manual control, as well as ThingSpeak for data logging and visualization.

## Features
- **Automated Irrigation**: Controls a water pump based on soil moisture levels and water availability.
- **Temperature & Humidity Monitoring**: Uses a DHT sensor to measure ambient conditions.
- **Fan Control**: Activates a fan if temperature exceeds 29°C or humidity is high.
- **Remote Control via Blynk**: Enables manual control and live updates through the Blynk mobile app.
- **LCD Display**: A 16x2 I2C LCD displays real-time sensor data (temperature, humidity, soil moisture, water level) and device status.
- **ThingSpeak Integration**: Sends sensor data to ThingSpeak for remote logging and visualization.
- **Wi-Fi Connectivity**: Connects the ESP32 to your local network for seamless data transmission.

## Components Used
- **ESP32 Microcontroller**
- **DHT Sensor (DHT11/DHT22)**: Measures temperature and humidity.
- **Soil Moisture Sensor**: Detects soil moisture levels.
- **Water Level Sensor**: Monitors water level in the tank.
- **Relay Module**: Controls the water pump and fan.
- **16x2 I2C LCD Display**: Displays sensor data and system status.
- **Blynk Mobile App**: Enables remote control and monitoring.
- **ThingSpeak API**: For logging and visualizing sensor data.

## File Structure
- `smart_irrigation_system.py`  
  The main script that:
  - Connects to Wi-Fi.
  - Initializes sensors (DHT, soil moisture, water level).
  - Sets up relay control for the water pump and fan.
  - Displays data on the I2C LCD.
  - Integrates with Blynk for remote control.
  - Sends sensor data to ThingSpeak.

- `BlynkLib.py`  
  Library for interfacing with the Blynk platform. Handles communication, virtual writes, and event processing.

- `dht.py`  
  Driver for the DHT sensor (supports DHT11/DHT22). Provides functions to measure temperature and humidity.

- `urequests.py`  
  A lightweight HTTP request library used to send sensor data to ThingSpeak.

- `i2c_lcd.py`  
  Driver for controlling a 16x2 I2C LCD using the PCF8574 expander. Handles low-level LCD commands and data writing.

- `lcd_api.py`  
  Provides a high-level API for interacting with HD44780-compatible LCD displays. Contains commands for display control, cursor movement, and custom character creation.

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Smart-Irrigation-System.git
cd Smart-Irrigation-System

### 2. Install Required Libraries

Ensure you have MicroPython set up on your ESP32. Use a tool like ampy or rshell to upload the files to your device. For example:
ampy --port /dev/ttyUSB0 put smart_irrigation_system.py
ampy --port /dev/ttyUSB0 put BlynkLib.py
ampy --port /dev/ttyUSB0 put dht.py
ampy --port /dev/ttyUSB0 put urequests.py
ampy --port /dev/ttyUSB0 put i2c_lcd.py
ampy --port /dev/ttyUSB0 put lcd_api.py

### 3. Configure the System

Wi-Fi Credentials: Update WIFI_SSID and WIFI_PASSWORD in smart_irrigation_system.py.

Blynk Authentication: Replace BLYNK_AUTH_TOKEN with your token from the Blynk app.

ThingSpeak API Key: Update THINGSPEAK_API_KEY with your key from ThingSpeak.

### 4. Run the System

Reset your ESP32 after uploading the files. Monitor the serial output to see sensor readings and system logs:
screen /dev/ttyUSB0 115200


### 5. How It Works

1. Wi-Fi Connection: The ESP32 connects to your local Wi-Fi network.

2. Sensor Measurements: The DHT sensor reads temperature and humidity, while the soil moisture and water level sensors provide real-time data.

3. Relay Control: Based on sensor readings:

  i) The water pump is activated if the soil is too dry and water level is sufficient.

  ii) The fan is activated if the temperature exceeds 29°C or humidity is high.

  iii) Manual control is available via Blynk.

4. Data Display: Sensor readings and relay statuses are displayed on the I2C LCD.

5. Remote Logging: Sensor data is sent to ThingSpeak using a simple HTTP GET request.

6. Blynk Integration: The system sends live updates to the Blynk app and responds to virtual pin commands for manual control.

### Future Enhancements:

i) Enhanced Data Visualization: Develop a web dashboard for more detailed data analysis.

ii) Notification System: Implement SMS or email alerts for critical sensor thresholds.

iii) Additional Sensors: Integrate more sensors for comprehensive environmental monitoring.

### License:

This project is open-source and available under the MIT License.

---

After pasting this content into your `README.md` file, save it. Then, follow the steps to add, commit, and push it to your GitHub repository (if you're using Git locally):

```bash
git add README.md
git commit -m "Add README.md with project details"
git push origin main

