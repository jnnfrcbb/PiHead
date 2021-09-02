## Contoller Service execution
```
controller_service [path]
```

use  **/etc/xdg/lxsession/LXDE-pi/autostart** to run Controller Service automatically at startup

---

## OpenAutoPro keystrokes:
|Key|Input|
|----|----|
|Up arrow|Navigate up|
|Down arrow|Navigate down|
|Left arrow|navigate left|
|Right arrow|Navigate right|
|1|Scroll/rotate left|
|2|Scroll/rotate right|
|Enter|Select|
|Escape|Back/Cancel|
|H|Home|
|P|Phone menu/answer call|
|O|Hang up call|
|X|Play|
|C|Pause|
|V|Previous track|
|B|Toggle play|
|N|Next track|
|G|Phone menu/answer call|
|J|Media menu|

## Android Auto keystrokes:

|Key|Input|
|---|---|
|Up arrow|Navigate up|
|Down arrow|Navigate down|
|Left arrow|Navigate left|
|Right arrow|Navigate right|
|1|Scroll/rotate left|
|2|Scroll/rotate right|
|Enter|Select|
|Escape|Back/Cancel|
|H|Home|
|P|Phone menu/answer call|
|O|Hang up call|
|X|Play|
|C|Pause|
|V|Previous track|
|B|Toggle play|
|N|Next track|
|M|Voice command|
|F|Launch navigation|
|G|Phone menu/anwer call|
|J|Launch media|

## Autobox (Apple CarPlay) keystrokes:

|Key|Input|
|---|---|
|Up arrow|Navigate up|
|Down arrow|Navigate down|
|1|Scroll/rotate left|
|2|Scroll/rotate right|
|Enter|Select|
|Escape|Back/Cancel|
|H|Home|
|X|Play|
|C|Pause|
|V|Previous track|
|B|Toggle play|
|N|Next track|
|M|Voice command|

## Global keystrokes:

|Key|Input|
|---|---|
|F2|Toggle Android Auto night mode|
|Ctrl+F3|Mode (toggle between active applications, projections and OpenAuto Pro interface)|
|F6|Expand/Collapse TopBar|
|F7|Volume down|
|F8|Volume up|
|F9|Brightness down|
|F10|Brightness up|
|Ctrl+F11|Toggle mute|
|F12|Bring OpenAuto Pro to front|

---

## Rotary encoder

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

## GPIO input

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

## BMW I-Drive Gen 1

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