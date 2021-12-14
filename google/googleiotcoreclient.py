import argparse
import datetime
import logging
import os
import random
import ssl
import time
import json
import jwt
import paho.mqtt.client as mqtt

# Created by Caleb Roelens, adapted from google cloud example codes.

class GoogleIotCoreCredentials:

    def __init__(self, project_id: str, cloud_region: str, registry_id: str, device_id: str, private_key_location: str,
                 root_ca_location: str, algorithm: str):
        """
        Credentials for the Google Iot Core.\n
        :param project_id:
        :param cloud_region:
        :param registry_id:
        :param device_id:
        :param private_key_location:
        :param root_ca_location:
        :param algorithm:
        """
        # Privatise params
        self.__project_id = project_id
        self.__cloud_region = cloud_region
        self.__registry_id = registry_id
        self.__device_id = device_id
        self.__private_key_location = private_key_location
        self.__root_ca_location = root_ca_location
        self.__algorithm = algorithm

    @property
    def project_id(self) -> str:
        return self.__project_id

    @project_id.setter
    def project_id(self, value: str):
        self.__project_id = value

    @property
    def cloud_region(self) -> str:
        return self.__cloud_region

    @cloud_region.setter
    def cloud_region(self, value: str):
        self.__cloud_region = value

    @property
    def registry_id(self) -> str:
        return self.__registry_id

    @registry_id.setter
    def registry_id(self, registry_id: str):
        self.__registry_id = registry_id

    @property
    def device_id(self) -> str:
        return self.__device_id

    @device_id.setter
    def device_id(self, device_id: str):
        self.__device_id = device_id

    @property
    def private_key_location(self) -> str:
        return self.__private_key_location

    @private_key_location.setter
    def private_key_location(self, private_key_location: str):
        self.__private_key_location = private_key_location

    @property
    def root_ca_location(self) -> str:
        return self.__root_ca_location

    @root_ca_location.setter
    def root_ca_location(self, root_ca_location: str):
        self.__root_ca_location = root_ca_location

    @property
    def algorithm(self) -> str:
        return self.__algorithm

    @algorithm.setter
    def algorithm(self, algorithm: str):
        self.__algorithm = algorithm


class GoogleIotCoreClientFunctions:

    def __init__(self, on_connect, on_publish, on_disconnect, on_message):
        self.__on_connect = on_connect
        self.__on_publish = on_publish
        self.__on_disconnect = on_disconnect
        self.__on_message = on_message

    @property
    def on_connect(self):
        return self.__on_connect

    @on_connect.setter
    def on_connect(self, on_connect):
        self.__on_connect = on_connect

    @property
    def on_publish(self):
        return self.__on_publish

    @on_publish.setter
    def on_publish(self, on_publish):
        self.__on_publish = on_publish

    @property
    def on_disconnect(self):
        return self.__on_disconnect

    @on_disconnect.setter
    def on_disconnect(self, on_disconnect):
        self.__on_disconnect = on_disconnect

    @property
    def on_message(self):
        return self.__on_message

    @on_message.setter
    def on_message(self, on_message):
        self.__on_message = on_message


class GoogleIotCoreClient:
    # INTERNAL PARAMS
    should_backoff = False
    MAXIMUM_BACKOFF_TIME = 32
    minimum_backoff_time = 1

    def __init__(self, credentials: GoogleIotCoreCredentials, functions: GoogleIotCoreClientFunctions, qos=1,
                 token_expire=60):
        print("Initiating class...")
        """
        Google Iot Core Client\n
        :param credentials: Credentials from GoogleIotCoreClient class
        :param functions: Functions for event from GoogleUIotCoreClientFunctions:
        :param qos: Qos (MQTT), default 1
        """
        self.__client = None
        self.__client: mqtt.Client
        self.__token_expire = token_expire
        self.__credentials = credentials
        self.__functions = functions
        self.__qos = qos
        self.__client_id = ""
        # Setup device
        self.__create_client()
        self.__setup_subs()
        # Run loop

    @property
    def client(self):
        return self.__client

    def __create_client(self) -> mqtt.Client:
        print("Creating client...")
        project_id = self.__credentials.project_id
        locations = self.__credentials.cloud_region
        registry_id = self.__credentials.registry_id
        device_id = self.__credentials.device_id
        # Set Client ID
        self.__client_id = f"projects/{project_id}/locations/{locations}/registries/{registry_id}/devices/{device_id}"
        # Create client
        self.__client = mqtt.Client(client_id=self.__client_id)
        # Create password for the Client to authenticate
        password = self.__create_password()
        # Apply new password
        self.__client.username_pw_set(username='unused', password=password)
        # Enable TLS support
        self.__client.tls_set(ca_certs=self.__credentials.root_ca_location)
        # Setup the function listeners
        self.__client.on_connect = self.__functions.on_connect
        self.__client.on_disconnect = self.__functions.on_disconnect
        self.__client.on_publish = self.__functions.on_publish
        self.__client.on_message = self.__functions.on_message
        # Connect to the MQTT Google Iot Core bridge
        self.__client.connect("mqtt.googleapis.com", 8883)
        # Setup config
        print("Client creation done.")
        return self.__client

    def loop_start(self):
        self.__client: mqtt.Client
        self.__client.loop_start()

    def __setup_subs(self):
        device_id = self.__credentials.device_id
        self.__client.subscribe(f"/devices/{device_id}/config", qos=1)
        self.__client.subscribe(f"/devices/{device_id}/commands/#", qos=0)

    def __create_password(self):
        print("Creating token...")
        # Create a JWT token using the certificate and an issuer date, audience and expire data.
        token = {
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self.__token_expire),
            "aud": self.__credentials.project_id
        }
        # Read the private key file
        with open(self.__credentials.private_key_location, 'r') as f:
            private_key = f.read()
        print("Token created.")
        return jwt.encode(token, private_key, algorithm=self.__credentials.algorithm)

    def subscribe(self, topic):
        # Subscribe to a topic
        self.__client: mqtt.Client
        new_sub = f"/devices/{self.__credentials.device_id}/{topic}"
        self.__client.subscribe(new_sub)
        print(f"GIC: Subscribed to topic {new_sub}")

    def publish(self, payload):
        self.__client: mqtt.Client
        topic_formatted = f"/devices/{self.__credentials.device_id}/events"
        print(f"Publishing to {topic_formatted}")
        self.__client.publish(topic=topic_formatted, payload=payload, qos=1)

    @staticmethod
    def error_str(rc):
        """Convert a Paho error to a human readable string."""
        return '{}: {}'.format(rc, mqtt.error_string(rc))

    @property
    def device_command_topic(self):
        return f"/devices/{self.__credentials.device_id}/commands"



