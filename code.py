import time
import board, busio, displayio
import adafruit_ds3231
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

metric = True # Set to False for degrees Fahrenheit

#Pin definitions for Raspberry Pi Pico
mosi_pin, clk_pin, reset_pin, cs_pin, dc_pin = board.GP11, board.GP10, board.GP17, board.GP18, board.GP16

days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

def c_to_f(celsius):
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit

def update_labels():
    global temperature
    minutes = "{:02}".format(t.tm_min)
    date_label.text = f"{days[int(t.tm_wday)]}, {t.tm_mday}/{t.tm_mon}/{t.tm_year}"
    time_label.text = f"{t.tm_hour}:{minutes}"
    temperature = round(rtc.force_temperature_conversion(),1)
    temperature_string = f"{temperature}°C"
    if not metric:
        temperature = round(c_to_f(temperature),1)
        temperature_string = f"{temperature}°F"
    
    temperature_value_label.text = temperature_string
    
    set_min_max_temperature()
    
    if metric:
        max_temperature_value_label.text = f"{str(max_temperature)}°C"
        min_temperature_value_label.text = f"{str(min_temperature)}°C"
    else:
        max_temperature_value_label.text = f"{str(max_temperature)}°F"
        min_temperature_value_label.text = f"{str(min_temperature)}°F"

    print(f"The date is {days[int(t.tm_wday)]} {t.tm_mday}/{t.tm_mon}/{t.tm_year}")
    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    print(f"Temperature: {temperature}")
    print(f"Min Temperature: {min_temperature}")
    print(f"Max Temperature: {max_temperature}")
    print(f"Temperature: {temperature}\n\n")

def set_min_max_temperature():
    global min_temperature, max_temperature
    if temperature > max_temperature:
        max_temperature = temperature
    if temperature < min_temperature:
        min_temperature = temperature

min_temperature = 100.0
max_temperature = 0.0
temperature = 0

font_file = "fonts/terminal.bdf"
font = bitmap_font.load_font(font_file)

displayio.release_displays()
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)
display = ST7735R(display_bus, width=128, height=160, bgr = True)

screen = displayio.Group()
display.show(screen)

# Create date label
date_label = label.Label(font, color=0x00FF00, text = "Date")
date_label.anchor_point = (0.5, 0.0)
date_label.anchored_position = (64, 5)

# Create time label
time_label = label.Label(font, color=0xFFFFFF)
time_label.anchor_point = (0.5, 0.0)
time_label.anchored_position = (64, 20)
time_label.scale = (3)

# Create temperature label
temperature_label = label.Label(font, color=0x00FF00, text = "TEMPERATURE")
temperature_label.anchor_point = (0.5, 0.0)
temperature_label.anchored_position = (64, 64)

# Create min_temperature label
min_temperature_label = label.Label(font, color=0x0000FF, text = "MIN")
min_temperature_label.anchor_point = (1.0, 0.0)
min_temperature_label.anchored_position = (110, 125)

# Create max_temperature label
max_temperature_label = label.Label(font, color=0xFF0000, text = "MAX")
max_temperature_label.anchor_point = (0.0, 0.0)
max_temperature_label.anchored_position = (18, 125)

# Create temperature value label
temperature_value_label = label.Label(font, color=0xFFFFFF)
temperature_value_label.anchor_point = (0.5, 0.0)
temperature_value_label.anchored_position = (64, 75)
temperature_value_label.scale = (3)

# Create max_temperature value label
max_temperature_value_label = label.Label(font, color=0xFFFFFF)
max_temperature_value_label.anchor_point = (0.0, 0.0)
max_temperature_value_label.anchored_position = (10, 140)

# Create min_temperature value label
min_temperature_value_label = label.Label(font, color=0xFFFFFF)
min_temperature_value_label.anchor_point = (1.0, 0.0)
min_temperature_value_label.anchored_position = (120, 140)
screen.append(min_temperature_value_label)
screen.append(max_temperature_value_label)
screen.append(time_label)
screen.append(date_label)
screen.append(temperature_value_label)
screen.append(max_temperature_label)
screen.append(min_temperature_label)
screen.append(temperature_label)

i2c = busio.I2C(board.GP1, board.GP0)
rtc = adafruit_ds3231.DS3231(i2c)
t = rtc.datetime

while True:
    t = rtc.datetime
    update_labels()
    time.sleep(1)  # wait a second