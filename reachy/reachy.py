# Runs on the raspberry Pi
# Move reachy using MQTT simple version, one move.
import time

import paho.mqtt
from reachy import Reachy
from reachy.parts import *
import paho
import paho.mqtt.client as mqtt

# PARAMS
io_mode = "ws"
hand_type = "force_gripper"  # What hand is attached to the reachy robot.


class ReachyExtended(Reachy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def action_right_arm_shoulder_roll(self, position: int, duration: float, wait: bool):
        self.right_arm.shoulder_roll.goto(goal_position=position, duration=duration, wait=wait)

    def action_left_arm_shoulder_roll(self, position: int, duration: float, wait: bool):
        self.left_arm.shoulder_roll.goto(goal_position=position, duration=duration, wait=wait)

    def action_right_arm_shoulder_pitch(self, position: int, duration: float, wait: bool):
        self.right_arm.shoulder_pitch.goto(goal_position=position, duration=duration, wait=wait)

    def action_left_arm_shoulder_pitch(self, position: int, duration: float, wait: bool):
        self.left_arm.shoulder_pitch.goto(goal_position=position, duration=duration, wait=wait)

    def action_set_one(self):
        self.action_right_arm_shoulder_roll(-90, 0.25, False)
        self.action_left_arm_shoulder_roll(90, 0.25, True)
        self.action_right_arm_shoulder_roll(90, 0.25, False)
        self.action_left_arm_shoulder_roll(-90, 0.25, True)
        self.action_left_arm_shoulder_pitch(-90, 0.25, False)
        self.action_right_arm_shoulder_pitch(90, 0.25, True)
        self.action_left_arm_shoulder_pitch(90, 0.25, False)
        self.action_right_arm_shoulder_pitch(-90, 0.25, True)


# MQTT
host = ""
port = 1883


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client: mqtt.Client
    client.subscribe("reachy/action")
    # Use these two action to keep the ws connection active.
    r.action_right_arm_shoulder_pitch(1, 0.01, False)
    r.action_left_arm_shoulder_pitch(0, 0.01, False)


r = ReachyExtended(LeftArm(io=io_mode, hand=hand_type),
                   RightArm(io=io_mode, hand=hand_type))


def on_message(client, userdata, msg):
    print("Received a message.")
    r.action_set_one()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port, 60)
client.loop_forever(10)
