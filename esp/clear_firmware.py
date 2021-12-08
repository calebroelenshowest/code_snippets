# Requires esptool installed and binary to flash in the execution folder.
# For ESP8266
port = input("Port: ")
import os
os.system(f"esptool.py --chip esp32 --port {port} erase_flash")
os.system(f"esptool.py --chip esp32 --port {port} --baud 460800 write_flash -z 0x1000 .\esp32-20210902-v1.17.bin")
