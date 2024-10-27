import math
from utils import play_beep


def kelvin_to_celcius_Fahrenheit(kelvin):
    celcius = kelvin - 273.15
    fahrenheit = celcius * (9/5) + 32
    return celcius, fahrenheit


def beaufort_scale_calculation(wind_speed, wind_gust):
    BScale_wind_speed = (wind_speed / 0.836) ** (2/3)
    BScale_wind_speed_rounded = math.floor(BScale_wind_speed)

    BScale_wind_gust = (wind_gust / 0.836) ** (2/3)
    BScale_wind_gust_rounded = math.floor(BScale_wind_gust)

    return BScale_wind_speed_rounded, BScale_wind_gust_rounded


def get_wind_direction(degree):
    if degree >= 337.5 or degree < 22.5:
        return "North"
    elif 22.5 <= degree < 67.5:
        return "North East"
    elif 67.5 <= degree < 112.5:
        return "East"
    elif 112.5 <= degree < 157.5:
        return "South East"
    elif 157.5 <= degree < 202.5:
        return "South"
    elif 202.5 <= degree < 247.5:
        return "South West"
    elif 247.5 <= degree < 292.5:
        return "West"
    elif 292.5 <= degree < 337.5:
        return "North West"


def assign_storm_type(utc_shift_seconds):
    hours_shift = utc_shift_seconds // 3600
    if hours_shift < 0:
        return "Hurricane"
    else: return "Typhoon"


def get_storm_category(beaufort_number, storm_type):
    categories = {}

    if storm_type == "Hurricane":
        categories.update({
            range(12, 14): f"Category 1 {storm_type}",
            range(14, 16): f"Category 2 {storm_type}",
            range(16, 17): f"Category 3 Major {storm_type}",
            range(17, 19): f"Category 4 Major {storm_type}",
            range(19, 38): f"Category 5 Major {storm_type}"
        })

    elif storm_type == "Typhoon":
        categories.update({
            range(12, 14): f"{storm_type}",
            range(14, 16): f"Very Strong {storm_type}",
            range(16, 19): f"Violent {storm_type}",
            range(19, 38): f"Super {storm_type}"
        })

    for beaufort_range, category in categories.items():
        if beaufort_number in beaufort_range:
            return category
    return None


def assign_wind_condition(beaufort_number, storm_type):
    wind_speed_conditions = {
        6: "Strong Breeze",
        7: "Near Gale",
        8: "Gale",
        9: "Severe Gale",
        10: "Storm",
        11: "Violent Storm"
    }

    wind_speed_condition = wind_speed_conditions.get(beaufort_number, "None")

    if beaufort_number > 11:
        wind_speed_condition = get_storm_category(beaufort_number, storm_type)
    
    return wind_speed_condition


def storm_alert(wind_speed_beaufort_number, wind_gust_beaufort_number):
    beep_amount = 0
    wait_time_offset = 0
    if wind_speed_beaufort_number >= 6 and wind_speed_beaufort_number <= 10:
        beep_amount = 1
        wait_time_offset = 0.5
    elif wind_speed_beaufort_number > 10: 
        beep_amount = 2
        wait_time_offset = 1

    if wind_speed_beaufort_number < wind_gust_beaufort_number:
        if wind_gust_beaufort_number >= 6 and wind_gust_beaufort_number <= 10:
            beep_amount = 1
            wait_time_offset = 0.5
        elif wind_gust_beaufort_number > 10:
            beep_amount = 2
            wait_time_offset = 1

    if beep_amount > 0: 
        play_beep(beep_amount)
        return wait_time_offset
    
    return 0
