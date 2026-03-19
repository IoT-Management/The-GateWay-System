import time

def process(obj):

    data = dict(obj.data)
    temp = int(data["temperature"])

    print("Temperature:", temp)

    if temp > 50:

        leds = [
            "/sys/class/leds/beaglebone:green:usr0/brightness",
            "/sys/class/leds/beaglebone:green:usr1/brightness",
            "/sys/class/leds/beaglebone:green:usr2/brightness",
            "/sys/class/leds/beaglebone:green:usr3/brightness"
        ]

        for led in leds:
            with open(led, "w") as f:
                f.write("1")

        print("All LEDs ON")
