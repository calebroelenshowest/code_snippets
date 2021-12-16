# This is for reading a default mqtt device
# Fast readouts, fast exports and filtered topics
import time

from paho.mqtt import client as mqtt


class MQTTFunctions:

    def __init__(self, on_message=None, on_publish=None, on_disconnect=None, on_connect=None, on_subscribe=None):
        self.__on_message = on_message
        self.__on_publish = on_publish
        self.__on_subscribe = on_subscribe
        self.__on_disconnect = on_disconnect
        self.__on_connect = on_connect

    @property
    def on_message(self):
        return self.__on_message

    @on_message.setter
    def on_message(self, value):
        self.__on_message = value

    @property
    def on_publish(self):
        return self.__on_publish

    @on_publish.setter
    def on_publish(self, value):
        self.__on_publish = value

    @property
    def on_connect(self):
        return self.__on_connect

    @on_connect.setter
    def on_connect(self, value):
        self.__on_connect = value

    @property
    def on_disconnected(self):
        return self.__on_disconnect

    @on_disconnected.setter
    def on_disconnected(self, value):
        self.__on_disconnect = value

    @property
    def on_subscribe(self):
        return self.__on_subscribe

    @on_subscribe.setter
    def on_subscribe(self, value):
        self.__on_subscribe = value


class MQTTDevice:

    def __init__(self, functions: MQTTFunctions, name):
        self.__client = mqtt.Client()
        self.__functions = functions
        self.__name = name

        self.__topics = {}

    def set_callback(self):
        print(f"Applying functions to client {self.__name}.")
        if self.__functions.on_connect is not None:
            self.__client.on_connect = self.__functions.on_connect
        if self.__functions.on_message is not None:
            self.__client.on_message = self.__functions.on_message
        if self.__functions.on_publish is not None:
            self.__client.on_publish = self.__functions.on_publish
        if self.__functions.on_subscribe is not None:
            self.__client.on_subscribe = self.__functions.on_subscribe
        if self.__functions.on_disconnected is not None:
            self.__client.on_disconnect = self.__functions.on_disconnected
        print(f"Functions applied to client {self.__name}")

    def enable_custom_callbacks(self):
        if self.__functions.on_message is None:
            self.__client.on_message = self.__on_message_custom

    def connect(self, *args) -> bool:
        """
        :param args: In order: hostname, port, timeout,
        :return: Error or no error
        """
        try:
            self.__client.connect(*args)
            return True
        except Exception as exe:
            print(f"{self.__name} client error while connecting: {exe}")
            return False


    def sub_to_topic(self, topic_string, callback_function=None):
        if self.__functions.on_message is None:
            if callback_function is None:
                print(f"client {self.__name} callback_function should not be not None if there is no on_message "
                      f"callback defined.")
            else:
                self.__topics[topic_string] = callback_function
                self.__client.subscribe("#")

    def __on_message_custom(self, *args):
        print(args)
        mqtt_client, userdata, message = args
        print(message.topic)
        for topic in list(self.__topics.keys()):
            if topic == message.topic:
                self.__topics[topic]()

    def activate_loop_start(self):
        self.__client.loop_start()


def bytes_to_string(bytes_string, encoding="utf-8"):
    return str(bytes_string, encoding).replace("'", "").replace("b", "")


if __name__ == "__main__":
    # Test code
    x_functions = MQTTFunctions()
    def on_connect_event(*args): print(f"on_connect: {args}")
    def all_messages(*args): print(f"on_all_message: {args}")
    x_functions.on_connect = on_connect_event
    client = MQTTDevice(x_functions, "smartswarm")
    client.connect("172.23.83.254", 1883, 60)
    client.enable_custom_callbacks()
    client.sub_to_topic("#", all_messages)
    client.activate_loop_start()
    while True:
        time.sleep(2)
