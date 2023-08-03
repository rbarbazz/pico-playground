import time
import ntptime
import network
import machine
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4

try:
    from env import WIFI_SSID, WIFI_PASSWORD
except ImportError:
    WIFI_SSID = None
    WIFI_PASSWORD = None


# Wifi - START
wlan = network.WLAN(network.STA_IF)


def connect_wifi(wifi_ssid=WIFI_SSID, wifi_password=WIFI_PASSWORD):
    """
    Connect to a WiFi network using the provided SSID and password.

    :param wifi_ssid: The SSID of the WiFi network to connect to.
    :type wifi_ssid: str
    :param wifi_password: The password of the WiFi network to connect to.
    :type wifi_password: str
    :raises RuntimeError: If the WiFi SSID or password is not provided.
    """
    if wifi_ssid is None or wifi_password is None:
        raise RuntimeError(
            "WiFi SSID/PASSWORD required."
            "Set them in env.py and copy it to your Pico, or pass them as arguments."
        )
    wlan.active(True)

    print(f"Connecting to {wifi_ssid}...")
    wlan.connect(wifi_ssid, wifi_password)

    while True:
        if wlan.isconnected():
            break
        time.sleep(0.2)
    print(f"Connected to {wifi_ssid}!")


def disconnect_wifi():
    """
    Disconnect from the WiFi network and deactivate the WLAN interface.
    """
    wlan.disconnect()
    wlan.active(False)


# Wifi - END

# Display - START

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
FONT_HEIGHT = 8
FONT_SCALE = 6
SCALED_FONT_HEIGHT = FONT_HEIGHT * FONT_SCALE
DISPLAY_WIDTH, DISPLAY_HEIGHT = display.get_bounds()


def clear_display():
    """
    Paint the screen black.
    """
    display.set_pen(BLACK)
    display.clear()
    display.update()


def setup_display():
    """
    Set up the display by setting the backlight to 70% and the font to "bitmap8".
    """
    display.set_backlight(0.7)
    display.set_font("bitmap8")
    clear_display()


# Display - END

# Time - START

rtc = machine.RTC()


def setup_time():
    """
    Set the current time on the RTC using NTP (Network Time Protocol).
    """
    ntptime.settime()


# Time - END


# Setup
setup_display()
connect_wifi()
setup_time()
disconnect_wifi()

UTC_OFFSET = -7

previous_formatted_time = ""

# Main loop
while True:
    year, month, day, wd, hour, minute, second, _ = rtc.datetime()
    hour = (hour + UTC_OFFSET) % 24
    formatted_time = f"{hour:02}:{minute:02}:{second:02}"

    if previous_formatted_time != formatted_time:
        text_width = display.measure_text(formatted_time, scale=FONT_SCALE)
        clear_display()
        display.set_pen(WHITE)
        display.text(
            formatted_time,
            # Center the text horizontally
            int((DISPLAY_WIDTH - text_width) / 2),
            int(
                # Center the text vertically
                (DISPLAY_HEIGHT - SCALED_FONT_HEIGHT)
                / 2
            ),
            scale=FONT_SCALE,
        )
        display.update()
        previous_formatted_time = formatted_time

    time.sleep(0.2)
