from machine import Pin, SoftI2C
import sh1106
import time

# Initialize I2C
scl = Pin(22, Pin.OUT, Pin.PULL_UP)
sda = Pin(21, Pin.OUT, Pin.PULL_UP)
i2c = SoftI2C(scl=scl, sda=sda, freq=400000)

# Initialize SH1106 OLED display
oled = sh1106.SH1106(i2c)

# Clear the display
oled.fill(0)
oled.show()

# Display text on the OLED
oled.text("Hello, Troynics!", 0, 0)
oled.text("MicroPython-ESP32", 0, 16)
oled.text("OLED Test", 0, 32)
oled.show()
time.sleep(4)

# Final message
oled.fill(0)
oled.text("Done!", 0, 0)
oled.show()
