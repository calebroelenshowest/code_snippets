# Console application
import time
from subprocess import call
import os
# Match the directory
# Requires GOOGLE_APPLICATION_CREDENTIALS
print(f"Current directory: {os.getcwd()}")

options = ["on", "off"]


def launch_with_params(file, cmd):

    args = ["--project_id=", "--cloud_region=europe-west1", "--registry_id=",
            "--device_id=", f"--send_command='{cmd}'", "send-command"]
    result = call(["python", f"{file}.py", *args])
    print(f"Code was {['successfully executed.', 'failed to execute'][result != 1]}")


while True:
    print("LED control program")
    print(f"Options: ", *options)
    input_cmd = input("Choice: ")
    if input_cmd.lower() in options:
        print("Inside")
        launch_with_params("send_command", input_cmd.lower())
    else:
        print("Outside")


