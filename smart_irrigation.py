import time
import dht
import urequests
from machine import Pin, ADC, I2C
import BlynkLib
import network
from i2c_lcd import I2cLcd  # Importing the custom I2C LCD driver

# Wi-Fi Credentials
WIFI_SSID = 'AD'
WIFI_PASSWORD = '123456789'

# Blynk Auth Token
BLYNK_AUTH_TOKEN = 'Your_Auth_Token'

# Wi-Fi Connection
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    print("Connected to Wi-Fi")
    return wlan

# Connect to Wi-Fi
connect_wifi() 
time.sleep(2)

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server="blynk.cloud", port=8080, insecure=True)

# ThingSpeak API Key and URL
THINGSPEAK_API_KEY = 'Your_THINGSPEAK_API_KEY'
THINGSPEAK_URL = f'http://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}'

# Initialize DHT Sensor
DHT_PIN = 4
sensor = dht.DHT11(Pin(DHT_PIN))

# Soil Moisture Sensor Pins
SOIL_MOISTURE_A0_PIN = 34
soil_moisture_analog = ADC(Pin(SOIL_MOISTURE_A0_PIN))
soil_moisture_analog.atten(ADC.ATTN_11DB)

# Water Level Sensor
WATER_LEVEL_PIN = 32
water_level_sensor = ADC(Pin(WATER_LEVEL_PIN))
water_level_sensor.atten(ADC.ATTN_11DB)

# Relay Pins
RELAY_PIN1 = 25
relay1 = Pin(RELAY_PIN1, Pin.OUT)
relay1.value(1)  # Start with pump OFF

RELAY_PIN2 = 23
relay2 = Pin(RELAY_PIN2, Pin.OUT)
relay2.value(1)  # Start with fan OFF

# Flags to control automation state
auto_pump_enabled = False
auto_fan_enabled = False


# I2C LCD Setup
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
I2C_ADDR = 0x27
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# ThingSpeak Update Function
def update_thingspeak(temp, hum, soil_moisture, water_level):
    try:
        url = THINGSPEAK_URL + f"&field1={temp}&field2={hum}&field3={soil_moisture}&field4={water_level}"
        response = urequests.get(url)
        response.close()
        #print("Data sent to ThingSpeak")
    except Exception as e:
        print("Failed to send data to ThingSpeak:", e)

# Manual Control for Pump and Fan through Blynk
@blynk.on("V12")
def control_pump(value):
    global auto_pump_enabled
    if int(value[0]) == 1:
        auto_pump_enabled = True
    else:
        auto_pump_enabled = False
        relay1.value(1)  # Turn Pump OFF immediately when disabled
    blynk.virtual_write(12, 1 if relay1.value() == 0 else 0)  # Update Pump status on Blynk

@blynk.on("V10")
def control_fan(value):
    global auto_fan_enabled
    if int(value[0]) == 1:
        auto_fan_enabled = True
    else:
        auto_fan_enabled = False
        relay2.value(1)  # Turn Fan OFF immediately when disabled
    blynk.virtual_write(10, 1 if relay2.value() == 0 else 0)  # Update Fan status on Blynk

# Main Loop
counter = 0
while True:
    try:
        blynk.run()
        time.sleep(2)
        
        # DHT11 Temperature & Humidity
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Soil Moisture
        soil_moisture_value = soil_moisture_analog.read()
        soil_moisture_percentage = ((4095 - soil_moisture_value) / 4095) * 100
        soil_status = "Too Wet" if soil_moisture_percentage >= 75 else "Wet" if 50 <= soil_moisture_percentage < 75 else "Dry" if 25 <= soil_moisture_percentage < 50 else "Too Dry"

        # Water Level
        water_level_value = water_level_sensor.read()
        water_level_percentage = (water_level_value / 4095) * 100
        
        # Automatic Control of Pump
        if auto_pump_enabled:
            if soil_moisture_percentage < 50 and water_level_percentage > 10:
                relay1.value(0)  # Pump ON
            else:
                relay1.value(1)  # Pump OFF
        pump_status = 1 if relay1.value() == 0 else 0

        # Automatic Control of Fan
        if auto_fan_enabled:
            if temperature > 29 or humidity > 40:
                relay2.value(0)  # Fan ON
            else:
                relay2.value(1)  # Fan OFF
        fan_status = 1 if relay2.value() == 0 else 0

        # Console and LCD Output
        print(f"Reading {counter}: Temp: {temperature}°C, Humidity: {humidity}%, Soil: {int(soil_moisture_percentage)}%, Status: {soil_status}, Water: {int(water_level_percentage)}%, PUMP: {pump_status}, FAN: {fan_status}")
        # Display all data on a single LCD screen
        lcd.clear()
        lcd.putstr(f"T:{temperature}C H:{humidity}% M:{soil_moisture_percentage:.0f}%")
        lcd.move_to(0, 1)
        lcd.putstr(f"W:{water_level_percentage:.0f}%  P:{pump_status}  F:{fan_status}")

        # Send data to ThingSpeak
        update_thingspeak(temperature, humidity, int(soil_moisture_percentage), int(water_level_percentage))

        # Send data to Blynk
        blynk.virtual_write(0, temperature)
        blynk.virtual_write(1, humidity)
        blynk.virtual_write(2, soil_moisture_percentage)
        blynk.virtual_write(3, water_level_percentage)
        blynk.virtual_write(12, pump_status)
        blynk.virtual_write(10, fan_status)

        # Increment counter
        counter += 1
        time.sleep(15)

    except OSError as e:
        lcd.clear()
        lcd.putstr("Sensor Error")
        print("Sensor Error:", e)
        time.sleep(1)
    except Exception as e:
        print("General Error:", e)
        time.sleep(2)
