import board
import digitalio
import analogio
import usb_hid
from time import sleep

from hid_gamepad import Gamepad

gp = Gamepad(usb_hid.devices)

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

twistIt = board.GP0
pullIt = board.GP1
spinIt = board.GP2
flickIt = board.GP18
bopIt_green = board.GP3
bopIt_yellow = board.GP4

camReset = Keycode.Q
roll = Keycode.SPACE
jump = Keycode.F
crouch = Keycode.X
r1 = Keycode.ONE
r2 = Keycode.TWO
L1 = Keycode.THREE
L2 = Keycode.FOUR
drink = Keycode.R
action = Keycode.E
itemSwitch = Keycode.DOWN_ARROW

button_pins = (twistIt, pullIt, spinIt,
               bopIt_yellow, flickIt)

keyboard_buttons1 = {0 : r1, 1 : r2, 2 : action,
                    3 : roll, 4 : camReset}

keyboard_buttons2 = {0 : L1, 1 : itemSwitch, 2 : jump,
                    3 : drink, 4 : camReset}

layer = 1
layerMax = 2

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]

layerButton_pin = bopIt_green
layerButton = digitalio.DigitalInOut(layerButton_pin)
layerButton.direction = digitalio.Direction.INPUT
layerButton.pull = digitalio.Pull.UP

for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    
ax = analogio.AnalogIn(board.GP27)
ay = analogio.AnalogIn(board.GP26)

def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    if not layerButton.value:
        layer = layer + 1
        if layer > layerMax:
            layer = 1
        sleep(0.2)
                                                                                                                                            
    if layer == 1:       
        for i, button in enumerate(buttons):
            if button.value:
                keyboard.release(keyboard_buttons1[i])
            else:
                keyboard.press(keyboard_buttons1[i])
       
    if layer == 2:
        for i, button in enumerate(buttons):
            if button.value:
                keyboard.release(keyboard_buttons2[i])
            else:
                keyboard.press(keyboard_buttons2[i])
        
    gp.move_joysticks(
        x=(range_map(ax.value, 0, 65535, -127, 127)) * -1,
        y=range_map(ay.value, 0, 65535, -127, 127),
    )
    print("x", ax.value, "y", ay.value, "Layer", layer) 