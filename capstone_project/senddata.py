import serial
import time

arduino = serial.Serial(port='COM14', baudrate=115200, timeout=2)  # Increased timeout to 2 seconds
time.sleep(0.5)
data = arduino.read_until(b'\n')
print("Received:", data.decode("ascii")) 

def push(x):
    y = str(x) + "\n"
    arduino.write(y.encode("ascii"))  # Send the encoded string to Arduino
    #print(x)
    # Read response from Arduino
    #data = arduino.read_until(b'\n')  # Read response until newline character
    #print("Received:", data.decode("ascii"))  # Decode received bytes as ASCII string
    print(x)
    time.sleep(0.01)

def close():
    arduino.close
    print("closed")
