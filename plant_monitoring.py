import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import sched
import csv


# this will trigger the lights/ anything hooked up to the IOT
def ioton():
    #This initializes the GPIO pin that will be used ot activate the IOT switch
    PIN_GPIO = 17
 
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_GPIO, GPIO.OUT)
 
    GPIO.output(PIN_GPIO, True)
    print('Lights and fan have been turned on')

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
            print("Sensor failure. Check wiring.")
            time.sleep(3)
            current += 1

# When called, this function will output the data from the moisture sensor
def current_moisture():
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
        current_moisture()
     else:
        print('INVALID INPUT: Please enter START, STOP, or STATUS to get an update: ')

# This uses python's bulit in schedular to activate the IOT at sceduled times.
def run_daily_schedule():
    scheduler = sched.scheduler(time.time, time.sleep)
    
    # Define the function to be run at 8am
    def run_at_8am():
        print("The lights and fan were turned on at 8am!")
        ioton()
        
        scheduler.enterabs(get_next_run_time(17), 1, run_at_5pm) #Sets the 5pm scedule

    # Define the function to be run at 5pm
    def run_at_5pm():
        print("Scheduled shutdown has happened at 5pm!")
        iotoff()
        
        scheduler.enterabs(get_next_run_time(8), 1, run_at_8am) #sets the 8am schedule

    # Schedule the first run of the function at 8am
    scheduler.enterabs(get_next_run_time(8), 1, run_at_8am)
    
    # Start the scheduler
    scheduler.run()

def get_next_run_time(hour):
    current_time = time.time()
    current_datetime = time.localtime(current_time)

    # Set the hour of the next run time to the specified hour
    next_run_datetime = time.struct_time((current_datetime.tm_year, current_datetime.tm_mon, current_datetime.tm_mday, hour, 0, 0, current_datetime.tm_wday, current_datetime.tm_yday, current_datetime.tm_isdst))
    next_run_time = time.mktime(next_run_datetime)
    
    # If the next run time is in the past, add a day to the next run time
    if next_run_time < current_time:
        next_run_time += 86400
    
    return next_run_time

def log_sensor_data():
    # Code to read temperature, humidity, and moisture data goes here
    temperature = get_temperature_and_humidity()
    moisture = get_moisture()
    
    # Code to log the data goes here
    log_data(temperature, humidity, moisture)

def get_temperature_and_humidity():
    temperature = 25.0
    return temperature

def get_humidity():
    humidity = 50.0
    return humidity

def get_moisture():
    moisture = 75.0
    return moisture

def log_data(temperature, humidity, moisture):
    with open("sensor_data.csv", mode="a") as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        
        # Write the sensor data to the CSV file
        writer.writerow([temperature, humidity, moisture, time.time()])
        
    # Print a message to indicate that the data has been logged
    print("Sensor data logged to CSV file")

def start_sensor_logging():
    # Schedule the logging function to run at the beginning of each hour
    schedule.every().hour.at(":00").do(log_sensor_data)
    
    # Start the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)


# This function will run at the beginning of the program and start prompting the user
run_daily_schedule()
command()