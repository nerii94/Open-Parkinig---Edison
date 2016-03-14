import time
import pyupm_grove as grove
import pyupm_buzzer as upmBuzzer
import pyupm_i2clcd as lcd

# Create the button object using GPIO pin 0
button = grove.GroveButton(4)
buzzer = upmBuzzer.Buzzer(8)
myLcd = lcd.Jhd1313m1(4, 0x3E, 0x62)

myLcd.setCursor(0,0)
# RGB Blue
#myLcd.setColor(53, 39, 249)

# RGB Red
myLcd.setColor(255, 0, 0)

myLcd.write('Hello World')


# Read the input and print, waiting one second between readings
while 1:
          if (button.value() != 0):
                    buzzer.playSound(upmBuzzer.DO, 1000000)
          time.sleep(1)

# Delete the button object
del button
# Delete the buzzer object
del buzzer
