import json
from paho.mqtt import client as mqtt
import google_lib
from google_lib.googleiotcore import *
# Change this imports to your path to the file and import all (*)


# Functions
def on_message(client, userdata, message):
    print("On message")
    print(message.topic)


def on_publish(result, mid):
    print("On publish")
    print("Publish: ", GoogleIotCoreClient.error_str(mid))


def on_connected(client, userdata, flags, rc):
    print(f"Connected with code: {rc}")


def on_disconnected(client, userdata, rc):
    print("On disconnected")
    print("Disconnected: ", GoogleIotCoreClient.error_str(rc))


my_functions = GoogleIotCoreClientFunctions(on_connect=on_connected, on_disconnect=on_disconnected,
                                            on_message=on_message, on_publish=on_publish)

my_credentials = GoogleIotCoreCredentials(project_id="", cloud_region="europe-west1",
                                          registry_id="", device_id="",
                                          private_key_location="rsa_private_gcp.pem", algorithm="RS256",
                                          root_ca_location="roots.pem")

my_client = GoogleIotCoreClient(credentials=my_credentials, functions=my_functions, qos=1, token_expire=60)
my_client.loop_start()
while True:
    my_client.publish(json.dumps({"sensorvalue": 20, "device_id": my_credentials.device_id}))
    time.sleep(5)
