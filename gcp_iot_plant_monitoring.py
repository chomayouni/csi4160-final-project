# ------------------------------------------------------------------------
# Original project: https://github.com/Ivan-koz/GC-IoT_Python_example
# ------------------------------------------------------------------------
import datetime
import json
import os
import ssl
import time

import jwt
import paho.mqtt.client as mqtt

# ------------------------------------------------------------------------
# CSI 4160: Need to change the sensor/actuator pins to be Assignment 1
# Can create different variables too depending on what you're using
import RPi.GPIO as GPIO

# Used pins (note that these are GPIO pins, not the physical pins)
RED_LED_PIN = 18
GREEN_LED_PIN = 17
BUTTON_PIN = 21
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# CSI 4160: Replace these variables with your GCP parameters 
project_id = 'salehian-csi4160-w2023'       # Your project ID.
registry_id = 'salehian-csi4160'       # Your registry name.
device_id = 'salehian-csi4160-pi'  # Your device name.
# ------------------------------------------------------------------------
private_key_file = 'rsa_private.pem'  # Path to private key.
algorithm = 'RS256'  # Authentication key format.
cloud_region = 'us-central1'  # Project region. Changed from original.
ca_certs = 'roots.pem'  # CA root certificate path.
mqtt_bridge_hostname = 'mqtt.googleapis.com'  # GC bridge hostname.
mqtt_bridge_port = 8883  # Bridge port.
message_type = 'event'  # Message type (event or state).

def create_jwt(project_id, private_key_file, algorithm):
    # Create a JWT (https://jwt.io) to establish an MQTT connection.
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    # Convert a Paho error to a human readable string.
    return '{}: {}'.format(rc, mqtt.error_string(rc))


class Device(object):
    # Device implementation.
    # this will trigger the lights/ anything hooked up to the IOT
    def ioton():
        #This initializes the GPIO pin that will be used ot activate the IOT switch
        PIN_GPIO = 17
        current_time = datetime.datetime.now()
    
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_GPIO, GPIO.OUT)
 
        GPIO.output(PIN_GPIO, True)
        print('Lights and fan have been turned on')
        print("the current date and time is: ", current_time)
    

    # this will turn off the lights/ anything hooked up to the IOT
    def iotoff():
    #This initializes the GPIO pin that will be used ot activate the IOT switch
        PIN_GPIO = 17
 
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_GPIO, GPIO.OUT)
 
        GPIO.output(PIN_GPIO, False)
        print('Lights and fan have been turned off')

    # When called, this function will output the data from the moisture sensor
    def humidity():
        #GPIO setup
        DHT_SENSOR = Adafruit_DHT.DHT11
        DHT_PIN = 4
    
        current = 1
        end = 10

        # This should probably be changed to and if statement so that it doesn't bug out when called
        while current <= end:
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                print("Temp={0:0.1f}C  Humidity={1:0.1f}%".format(temperature, humidity))
                current += 1
            else:
                print("Retrieving Data...")
                time.sleep(3)
                current += 1
        time_loop()

# When called, this function will output the data from the moisture sensor
    def is_soil_dry():
        #This code was taken from piddlerOnTheRoof's tutorial on youtube
        #GPIO setup
        PIN = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN)
    
        #  Reads the value from theGPIO pin
        moisture = GPIO.input(PIN)
    
        if moisture == 0:
            print("No water Detected! Your plants need to be watered")
        else:
            print("Soil moisture is nominal")


    #This function when called will prompt the users to enter a request 
    #This is meant to run tandam to the run_daily_schedule function and allows manual manipulation.
    def command():
        command = str.lower(input("Please enter START, STOP, or STATUS to get an update: "))

        if command == "start":
            print("Starting the plant monitoring system. Please stand by for readings.")
            ioton()
        
        elif command == "stop":
            print("Shutting off the lights")
            iotoff()
        elif command == "status":
            print("Displaying moisture and temperature data")
            humidity()
            is_soil_dry()
        else:
            print('INVALID INPUT: Please enter START, STOP, or STATUS to get an update: ')

    #This function handles the schedule of the plant monitoring system and pulls up the manual functions
    def time_loop():

        # loop works by checking if the current time has exceded the parameters in the if statements
        current_time = datetime.datetime.now().time()
        state = str.lower(input("The Plant Monitoring System schedule is in place. Should it run normally? Any custom shanges will be overidden by the system.  y/n: "))

        #The outermost if statement is put in place so that previous commands won't get overwritten automatiacally
        if state == "y":
            if current_time > datetime.time(8, 0):
                # Code to run if current time is greater than 8am goes here
                print("It's past 8am!")
                ioton()
            elif current_time > datetime.time(17, 0):
                # Code to run if current time is not greater than 8am goes here
                print("It's after 5pm!")
                iotoff()
            else:
                print("System initializing...")

            print("System clock has been checked. Plant Monitoring System has resumed scheduled functions")
        elif state == "n":
            print("continuing...")
        else:
            print("INVALID INPUT: Please enter enter y or n")
            time_loop()
    
        print("To adjust the system in real time you can enter the following commands:")
        print("START - will turn on the grow lights and fan ouside of working hours")
        print("STOP - will turn off the grow lights and fan inside of working hours")
        print("STATUS - will pull the current data from the Humidity,Temperature, and Moisture Sensors")
        command()

    def log_sensor_data():
        # Declare all of the pins that are used again because they aren't class variables
        DHT_SENSOR = Adafruit_DHT.DHT11
        DHT_PIN = 4
        MOISTURE_PIN = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOISTURE_PIN, GPIO.IN)

        # Get the three inputs
        humidity, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        moisture = GPIO.input(MOISTURE_PIN)

        # Organize the inputs in a list
        data = [temp, humidity, moisture]

        # Open the CSV file in append mode
        with open("output.csv", mode="a") as file:
            # Create a CSV writer object
            writer = csv.writer(file)
    
            # Write the data to the CSV file
            writer.writerow(data)
    # ------------------------------------------------------------------------

    def wait_for_connection(self, timeout):
        # Wait for the device to become connected.
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            raise RuntimeError('Could not connect to MQTT bridge.')

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        # Callback on connection.
        print('Connection Result:', error_str(rc))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        # Callback on disconnect.
        print('Disconnected:', error_str(rc))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        # Callback on PUBACK from the MQTT bridge.
        print('Published message acked.')

    def on_subscribe(self, unused_client, unused_userdata, unused_mid,
                     granted_qos):
        # Callback on SUBACK from the MQTT bridge.
        print('Subscribed: ', granted_qos)
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        # Callback on a subscription.
        payload = message.payload.decode('utf-8')
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(payload, message.topic, str(message.qos)))
        
        if not payload:
            return
        # Parse incoming JSON.
        data = json.loads(payload)
        # ------------------------------------------------------------------------
        # CSI 4160: If you receive a message from GCP, need to interpret it
        # If the red LED (led1) is different than the message received, then
        # update the field with the new message
        if data['led1'] != self.led1:
            self.led1 = data['led1']
            # Print status message to your Pi console
            if self.led1:
                print('Led1 is on')
            else:
                print('Led1 is off')

        # If the green LED (led2) is different than the message received from GCP,
        # then update the field with the new messge
        if data['led2']!=self.led2:
            self.led2 = data['led2']
            # Print status message to your Pi console
            if self.led2:
                print('Led2 is on')
            else:
                print('Led2 is off')
        # ------------------------------------------------------------------------
           
def main():

    client = mqtt.Client(
        client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id,
            cloud_region,
            registry_id,
            device_id))
    client.username_pw_set(
        username='unused',
        password=create_jwt(
            project_id,
            private_key_file,
            algorithm))
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    device = Device()

    client.on_connect = device.on_connect
    client.on_publish = device.on_publish
    client.on_disconnect = device.on_disconnect
    client.on_subscribe = device.on_subscribe
    client.on_message = device.on_message
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)
    client.loop_start()

    mqtt_telemetry_topic = '/devices/{}/events'.format(device_id)
    mqtt_config_topic = '/devices/{}/config'.format(device_id)

    # Wait up to 5 seconds for the device to connect.
    device.wait_for_connection(5)

    client.subscribe(mqtt_config_topic, qos=1)
    
    num_message = 0
    try:        
        # This function will run at the beginning of the program and start prompting the user
        while True:
            time_loop()
            log_sensor_data()
            

    except KeyboardInterrupt:
        # Exit script on ^C.
        pass
        # ------------------------------------------------------------------------
        # CSI 4160: When you exit, turn off both LEDs
        # Will need to change this if you have different setup
        GPIO.output(GREEN_LED_PIN,GPIO.LOW)
        GPIO.output(RED_LED_PIN,GPIO.LOW)

        # Clean up GPIO (good idea to keep this line)
        GPIO.cleanup()
        # ------------------------------------------------------------------------
        client.disconnect()
        client.loop_stop()
        print('Exit with ^C. Goodbye!')
        

if __name__ == '__main__':
    main()