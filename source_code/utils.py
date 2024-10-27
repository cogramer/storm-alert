import platform, os
from datetime import datetime, timezone, timedelta

def play_beep(beep_amount):
    while beep_amount > 0:
        system = platform.system()

        if system == "Windows":
            import winsound
            winsound.Beep(1000, 500) # 900 Hz, 500 ms

        elif system == "Linux":
            if os.system("command -v beep") == 0:
                os.system("beep -f 1000 -l 500")
            else:
                print("\a")

        elif system == "Darwin":
            os.system('afplay /System/Library/Sounds/Ping.aiff')

        beep_amount -= 1


def calculate_local_time(utc_shift_seconds):
    utc_now = datetime.now(timezone.utc)
    time_shift = timedelta(seconds=utc_shift_seconds)
    local_time = utc_now + time_shift
    return local_time

