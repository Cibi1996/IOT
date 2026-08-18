# Project 01 — LED Blink with Raspberry Pi Zero 2 W

## Overview

My first hands-on IoT project using a Raspberry Pi Zero 2 W.

The goal was to control an LED using a Raspberry Pi GPIO pin and Python.

## Objective

* Understand Raspberry Pi GPIO
* Control a digital output
* Learn basic breadboard wiring
* Use a resistor to protect an LED
* Write and run a Python GPIO program

## Hardware

* Raspberry Pi Zero 2 W
* Breadboard
* Green LED
* 330 Ω resistor
* Jumper wires

## Circuit

The LED was connected to GPIO17 through a 330 Ω current-limiting resistor.

```text
GPIO17 (Physical Pin 11)
        │
        ▼
     330 Ω
        │
        ▼
LED Anode (+)
LED Cathode (-)
        │
        ▼
GND (Physical Pin 6)
```

### Connections

| Raspberry Pi                | Breadboard / Component   |
| --------------------------- | ------------------------ |
| GPIO17 — Pin 11             | 330 Ω resistor           |
| Resistor                    | LED long leg / Anode (+) |
| LED short leg / Cathode (-) | GND                      |
| GND — Pin 6                 | Ground rail              |

## Software

* Raspberry Pi OS
* Python 3.13.5
* GPIO Zero

## Code

```python
from gpiozero import LED
from time import sleep

led = LED(17)

try:
    while True:
        led.on()
        sleep(1)

        led.off()
        sleep(1)

except KeyboardInterrupt:
    led.off()
```

## How It Works

The Python program controls GPIO17.

When GPIO17 is HIGH, current flows through the 330 Ω resistor and LED, causing the LED to turn on.

When GPIO17 is LOW, the LED turns off.

The program repeats this process every second.

## Testing

The project was successfully tested on the Raspberry Pi Zero 2 W.

### Result

The LED successfully blinked:

**ON → 1 second → OFF → 1 second → repeat**

## Troubleshooting

During the initial setup, the LED did not respond to the first GPIO test.

The circuit and GPIO connection were checked, and GPIO17 was tested directly.

The GPIO Zero library was then used to control GPIO17, after which the LED worked successfully.

This debugging process helped confirm the difference between:

* GPIO pin numbering
* Physical pin numbering
* GPIO output
* Breadboard power rails
* Software GPIO control

## What I Learned

* Raspberry Pi GPIO pins can be controlled using Python.
* GPIO17 corresponds to physical pin 11.
* Raspberry Pi GPIO operates at 3.3 V.
* An LED should be used with a current-limiting resistor.
* LED polarity matters.
* The longer LED leg is the anode (+).
* The shorter LED leg is the cathode (-).
* GPIO Zero provides a simple way to control Raspberry Pi GPIO devices.
* Debugging the hardware and software separately is important.

## Project Status

**Completed ✅**

## Photo

Project photo will be added here.

## Next

Project 02 will build on these GPIO fundamentals.

