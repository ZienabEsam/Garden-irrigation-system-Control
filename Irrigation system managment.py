import RPi.GPIO as GPIO
import bluetooth

# Setup
valve_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(valve_pin, GPIO.OUT)
GPIO.output(valve_pin, GPIO.LOW)

# Bluetooth server setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
bluetooth.advertise_service(server_sock, "IrrigationPi",
                            service_classes=[bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE])

print(f"Waiting for connection on RFCOMM channel {port}...")

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024).decode().strip()
        print(f"Received: {data}")

        if data == '1':
            GPIO.output(valve_pin, GPIO.HIGH)
            print("Valve turned ON")
        elif data == '0':
            GPIO.output(valve_pin, GPIO.LOW)
            print("Valve turned OFF")

except KeyboardInterrupt:
    print("Shutting down...")

finally:
    client_sock.close()
    server_sock.close()
    GPIO.cleanup()

