# PiHead

## GPIO Pins


| Row | No | Name | Function | | No | Name | Function |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 3.3V  |   |   | 2 | 5V |   |
| 2 | 3 | GPIO 2  | I2C SDA |   | 4 | 5V |   |
| 3 | 5 | GPIO 3  | I2C SCL |   | 6 | GND |   |
| 4 | 7 | GPIO 4  | 1 Wire  |   | 8 | GPIO 14 | 12V Input |
| 5 | 9 | GND  |   |   | 10 | GPIO 15 | Free (Sensor day/night signal) |
| 6 | 11 | GPIO 17 | 12V Input  |   | 12 | GPIO 18 | Free |
| 7 | 13 | GPIO 27 | 12V Output (OBD signal)  |   | 14 | GND |   |
| 8 | 15 | GPIO 22 | 12V Output (Amp signal)  |   | 16 | GPIO 23 | CAN INT |
| 9 | 17 | 3.3V  |   |   | 18 | GPIO 24 | ??  |
| 10 | 19 | GPIO 10 | CAN MOSI |   | 20 | GND |   |
| 11 | 21 | GPIO 9 | CAN MISO |   | 22 | GPIO 25 | PSU Latch |
| 12 | 23 | GPIO 11 | CAN SCLK |   | 24 | GPIO 8 | CAN CS |
| 13 | 25 | GND |   |   | 26 | GPIO 7 | Reverse |
| 14 | 27 | Reserved |  |   | 28 | Reserved  |   |
| 15 | 29 | GPIO 5 | Free |   | 30 | GND |   |
| 16 | 31 | GPIO 6 | Free |   | 32 | GPIO 12 | 12V Switched |
| 17 | 33 | GPIO 13 | Illumination |   | 34 | GND  |   |
| 18 | 35 | GPIO 19 | Free (Fan control) |   | 36 | GPIO 16 | Free |
| 19 | 37 | GPIO 26 | Free |   | 38 | GPIO 20 | Free |
| 20 | 39 | GND |   |   | 40 | GPIO 21 | Free |

RGB data: GPIO 18

RGB colours: GND = grey (to black); DATA = white (to white); VCC = green (to purple)

Light Sensor: SCL = blue ; SDA = green; GND = red; 3V = white


---

<br/>

## Contoller Service 

<br/>

### Execution
```
controller_service [path]
```

use  **/etc/xdg/lxsession/LXDE-pi/autostart** to run Controller Service automatically at startup



<br/>

### Rotary encoder

```
[Controller]
; Type of the input device
; 1 - Audi MMI 2G panel
; 2 - BMW iDrive Gen 1 controller
; 3 - BMW IBUS
; 4 - Audi RNSE
; 5 - Rotary Encoder
; 6 - GPIO
Type=5

[RotaryEncoder]
; GPIO pin number connected to the SIA/DT pin of the encoder
; For most rotary encoders you can control direction of the rotation by swapping SIA/DT abd SIB/CLK pins.
SiaPinNumber=16

; GPIO pin number connected to the the SIB/CLK pin of the encoder
; For most rotary encoders you can control direction of the rotation by swapping SIB/CLK and SIA/DT pins.
SibPinNumber=20

; GPIO pin number connected to the the SW pin of the encoder
SwPinNumber=21

; Key stroke that will be simulated after detection of left rotation
LeftKeyStrokes=V

; Key stroke that will be simulated after detection of right rotation
RightKeyStrokes=N

; Key stroke that will be simulated after detection of knob press/release
SwitchKeyStrokes=B
```

<br/>

### GPIO input

```
[Controller]
; Type of the input device
; 1 - Audi MMI 2G panel
; 2 - BMW iDrive Gen 1 controller
; 3 - BMW IBUS
; 4 - Audi RNSE
; 5 - Rotary Encoder
; 6 - GPIO
Type=6

; Transition from LOW to HIGH state simulates key press, transition from HIGH to LOW state simulates key release.
[GpioButtons]
; Number of configured GPIO pins
Count=3

; Number of 1st GPIO pin
Button_0_Pin=22

; Key stroke to simulate for 1st GPIO pin
Button_0_Key=F8

; Number of 2nd GPIO pin
Button_1_Pin=23

; Key stroke to simulate for 2nd GPIO pin
Button_1_Key=F7

; Number of 3rd GPIO pin
Button_2_Pin=16

; Key stroke to simulate for 3rd GPIO pin
Button_2_Key=N
```

<br/>

### BMW I-Drive Gen 1

```
[Controller]
; Type of the input device
; 1 - Audi MMI 2G panel
; 2 - BMW iDrive Gen 1 controller
; 3 - BMW IBUS
; 4 - Audi RNSE
; 5 - Rotary Encoder
; 6 - GPIO
Type=2

; CAN interface connected to the iDrive Gen 1 controller (e.g. via MCP2515 device)
Interface=can0

; Duration in milliseconds between two presses of the iDrive controller knob in left, right, up or down direction. 0 disables double press feature.
;
; List of double press actions:
;
; Right - [Mode - switch between active applications, OpenAuto Pro and active Projection (Android Auto or Mirroring)]
; Left - [Back]
; Up - [Show/Hide OpenAuto Pro Top Bar]
; Down - [Bring OpenAuto Pro to front]
DoublePressSpeed=200

[IDriveGen1]
; Orientation in degrees of the iDrive Gen 1 controller. Possible values are 0, 90, 180, 270.
Angle=0

; true - Enable standalone mode of the controller; false - listen controller connected to the CIC/CCC BMW head unit.
Polling=true

; Period in milliseconds of querying the iDrive Gen1 controller (standalone mode).
PollTimeout=100

; Timeout in milliseconds for response from the iDrive Gen 1 controller (standalone mode). Exceeding this timeout terminates the controller service.
ControllerTimeout=1000
```
---

<br/>

## Keystrokes

<br/>

### OpenAutoPro keystrokes:
|Key|Input|Code|
|----|----|----|
|Up arrow|Navigate up|
|Down arrow|Navigate down|
|Left arrow|navigate left|
|Right arrow|Navigate right|
|1|Scroll/rotate left|
|2|Scroll/rotate right|
|Enter|Select|
|Escape|Back/Cancel|
|H|Home|2|
|P|Phone menu/answer call|6|
|O|Hang up call|
|X|Play|
|C|Pause|
|V|Previous track|11|
|B|Toggle play|10|
|N|Next track|12|
|G|Phone menu/answer call|6|
|J|Media menu|4|

<br/>

### Android Auto keystrokes:

|Key|Input|Code|
|---|---|---|
|Up arrow|Navigate up|
|Down arrow|Navigate down|
|Left arrow|Navigate left|
|Right arrow|Navigate right|
|1|Scroll/rotate left|
|2|Scroll/rotate right|
|Enter|Select|
|Escape|Back/Cancel|
|H|Home|2|
|P|Phone menu/answer call|6|
|O|Hang up call|
|X|Play|
|C|Pause|
|V|Previous track|11|
|B|Toggle play|10|
|N|Next track|12|
|M|Voice command|9|
|F|Launch navigation|5|
|G|Phone menu/anwer call|6|
|J|Launch media|4|

<br/>

### Autobox (Apple CarPlay) keystrokes:

|Key|Input|Code|
|---|---|---|
|Up arrow|Navigate up|
|Down arrow|Navigate down|
|1|Scroll/rotate left|
|2|Scroll/rotate right|
|Enter|Select|
|Escape|Back/Cancel|
|H|Home|
|X|Play|
|C|Pause|
|V|Previous track|11|
|B|Toggle play|10|
|N|Next track|12|
|M|Voice command|9|

<br/>

### Global keystrokes:

|Key|Input|Code|
|---|---|---|
|F2|Toggle Android Auto night mode|7|
|Ctrl+F3|Mode (toggle between active applications, projections and OpenAuto Pro interface)|3|
|F6|Expand/Collapse TopBar|
|F7|Volume down|21|
|F8|Volume up|22|
|F9|Brightness down|
|F10|Brightness up|
|Ctrl+F11|Toggle mute|20|
|F12|Bring OpenAuto Pro to front|
