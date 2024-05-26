# Jakob Zielinski
# A test for pimenu


import time
import subprocess
import RPi.GPIO as GPIO
import atexit

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from pimenu import *
import helpers


def main():
    # Cleanup GPIO at program exit
    def exit_handler():
        print('Cleaning up GPIO before exit...')
        GPIO.cleanup()

    atexit.register(exit_handler)

    # Create the I2C interface.
    i2c = busio.I2C(SCL, SDA)

    # Create the SSD1306 OLED class.
    # The first two parameters are the pixel width and pixel height.  Change these
    # to the right size for your display!
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    # Clear display.
    disp.fill(0)
    disp.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    global cur_menu
    cur_menu=None

    # Callback for down button
    def button1_callback(channel):
        if GPIO.input(22):
            cur_menu.move_down()
            time.sleep(0.2)
        else:
            pass

    # Callback for enter button
    def button2_callback(channel):
        if GPIO.input(23):
            cur_menu.current_option().execute()
            time.sleep(0.2)
        else:
            pass

    # Callback for up button
    def button3_callback(channel):
        if GPIO.input(24):
            cur_menu.move_up()
            time.sleep(0.2)
        else:
            pass

    # Setup GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    # Down button
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(22, GPIO.BOTH, callback=button1_callback)
    # Enter button
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(23, GPIO.BOTH, callback=button2_callback)
    # Up Button
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(24, GPIO.BOTH, callback=button3_callback)

    # Function to change the current menu
    cur_menu = None
    def change_menu(m):
        global cur_menu
        cur_menu=m

    # Dummy menus to prevent errors
    main_menu=menu()
    sysinfo_menu=menu()
    hid_menu=menu()
    ping_menu=menu()
    ip_menu=menu()
    select_num_menu=menu()

    # Set up the main menu
    main_menu.add_option(option('System Info', change_menu, args=[sysinfo_menu]))
    main_menu.add_option(option('HID', print))
    main_menu.add_option(option('Ping', change_menu, args=[ping_menu]))
    main_menu.add_option(option('Reboot', helpers.reboot))
    main_menu.add_option(option('Shutdown', helpers.shutdown))

    sysinfo_menu.add_option(option('1', change_menu, args=[main_menu]))
    sysinfo_menu.add_option(option('2', change_menu, args=[main_menu]))
    sysinfo_menu.add_option(option('3', change_menu, args=[main_menu]))
    sysinfo_menu.add_option(option('4', change_menu, args=[main_menu]))
    sysinfo_menu.update_execute(helpers.sysinfo_update)

    ping_menu.add_option(option('1.1.1.1: ', change_menu, args=[main_menu]))
    ping_menu.add_option(option('Change IP Address', change_menu, args=[ip_menu])
    ping_menu.update_execute(helpers.ping, args=['1.1.1.1'])

    # Establish the main menu as the current menu
    cur_menu=main_menu
    
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Draw the menu options for the current menu
        for i in range(len(cur_menu.options[cur_menu.current:])):
            if i == 0:
                s = ' > '+cur_menu.options[i+cur_menu.current].string
            else:
                s = cur_menu.options[i+cur_menu.current].string
            draw.text((x, top+i*8), s, font=font, fill=255)

        # Execute the the action for the current menu
        cur_menu.execute(cur_menu, cur_menu.args)

        # Display image.
        disp.image(image)
        disp.show()
        time.sleep(0.1)


if __name__ == '__main__':
    main()


