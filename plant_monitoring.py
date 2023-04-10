import RPi.GPIO as GPIO
import Adafruit_DHT
import time


# this will trigger the lights/ anything hooked up to the IOT
def ioton():
    PIN_GPIO = 17
 
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_GPIO, GPIO.OUT)
 
    GPIO.output(PIN_GPIO, True)
    print('Lights and fan have been turned on')

# this will turn off the lights/ anything hooked up to the IOT
def iotoff():
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
            print("Sensor failure. Check wiring.")
            time.sleep(3)
            current += 1

# When called, this function will output the data from the moisture sensor
def moisture():
    #This code was taken from piddlerOnTheRoof's tutorial on youtube
    #GPIO setup
    channel = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN)
 
    def callback(channel):
            if GPIO.input(channel):
                    print("No water Detected!")
            else:
                    print("Water Detected!")
    # let us know when the pin goes HIGH or LOW
    GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  
     # assign function to GPIO PIN, Run function on change
    GPIO.add_event_callback(channel, callback) 
 
    # infinite loop
    while True:
            time.sleep(1)


def command():
     command = str.upper(input("Please enter START, STOP, or STATUS to get an update: "))

     if command == "start":
        print("Starting the plant monitoring system. Please stand by for readings.")
        ioton()
        
     elif command == "stop":
        print("Shutting off the lights")
        iotoff()
     elif command == "status":
        print("Displaying moisture and temperature data")
        humidity()
        moisture()
     else:
        print('INVALID INPUT: Please enter START, STOP, or STATUS to get an update: ')

#this function will run at the beginning of the program and start prompting the user
command()