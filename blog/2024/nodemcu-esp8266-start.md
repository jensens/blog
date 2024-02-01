---
blogpost: true
date: Jan 31, 2024
author: Jens W. Klein
location: Austria
category: Microcontroller
language: en
---


# Beginner-things I found about the ESP8266/ NodeMCU

I have some ideas what to do with my NodeMCU boards.
I need to learn how to use them and how to program them.

## First steps

I do not start at zero, I have some experience with Arduino and C++.
I am a professional programmer and now how to solve problems, but some information is hidden deeper in the internet than I expected.

ArduinoIDE is not my favorite IDE, so I use Visual Studio Code with the Platform.io extension.
But I use the Arduino Library with the ESP8266.

## Programming

First I started with some simple tasks, not related to hardware.
- Setup Wifi (easy)
- Setup NTP (kind of easy too)
- Use a library and refresh my C++ skills.
  I want to build a simple LED-strip based lamp with different moods dependening on the sunriset and sunset times.
  I found the [sunset lib](http://buelowp.github.io/sunset/html/index.html) and started to create an struct to hold the data and refresh it every day.
- Improve programming skills with C++ on NodeMCU, look for best practices and so on.

Then I started with some hardware related tasks.

## Pinout

Lessons learned about NodeMCU and ESP8266 pinouts:

First it is a good idea to print the pinout plan of the board you use.
Mine is a NodeMCU V3 and [TeachMeMicro has a good Pinout Reference](https://teachmemicro.com/nodemcu-pinout/).
But there are plenty other around.

Seconds you want to know how to use the pins.
[A Beginner's Guide to the ESP8266](https://tttapa.github.io/ESP8266/Chap01%20-%20ESP8266.html) has a great [ESP8266 Microcontroller overview with all pins and communication](https://tttapa.github.io/ESP8266/Chap02%20-%20Hardware.html).


## Power supply

The NodeMCU has a USB port and can be powered by USB.
This is 5V input.
Alternatively you can use the Vin pin and supply 5V there.

Internally ESP8266 uses 3.3V.
It has a voltage regulator on board, so you supply 5V via USB or to the Vin pin and it will be converted to 3.3V.

All inputs need to be 3.3V. More just destroys it.

## Motion sensor

Getting a motion sensor to work was a bit tricky.
I use a MH-SR602 PIR Motion Sensor. It has 3 pins: VCC, GND and OUT.
OUT is always lo and on motion detection is get hi for 2.5s.
Then it goes lo again.
I found an explaining [video about SR602](https://www.youtube.com/watch?v=Ho8oLNZkQF8).

First I implemented a check in the loop function, against the `millis()` function and a prev value to get the motion state.
I need more than 2.5s light, so I need to check for high, and after it goes low wait my time minus 2.5s and then check again.
Well, this is cumbersome.

Then I found [Interrupts](https://randomnerdtutorials.com/interrupts-timers-esp8266-arduino-ide-nodemcu/)  - well, sure! The interrupt goes out at the moment the pin changes to a selected state and triggers a function.
This made my code way simpler.

But it did not work.

I found out, that GPIO16 can not be used for interrupts.
This took me a while.
Switching over to a different pin solved the problem.

This is the code I use now:

```c++
#include <Arduino.h>

const int PIR_INPUT = D1; // PIR Sensor, don't use D0 (GPIO16)!
int motionDetected = 0;

void IRAM_ATTR detectsMovement()
{
    Serial.println("MOTION DETECTED!!!");
    motionDetected = millis();
    digitalWrite(LED_BUILTIN, LOW);
}

void setup()
{
    Serial.begin(115200);
    pinMode(PIR_INPUT, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(PIR_INPUT), detectsMovement, FALLING);
}

void loop()
{
    if ((motionDetected > 0) & (millis() - motionDetected > 10000))
    {
        Serial.println("Switch off!");
        motionDetected = 0;
        digitalWrite(LED_BUILTIN, HIGH);
    }
}
```

## Examples on the Web

There are plenty of code examples available.
And a ton of them are rubbish.

One good site (among others) is [ESP8266 Projects](https://lastminuteengineers.com/electronics/esp8266-projects/) by Last Minute Engineers. It has a good collection of starter examples.
Another one with helpful examples is [Random Nerd Tutorials ESP8266 projects](https://randomnerdtutorials.com/projects-esp8266/).

