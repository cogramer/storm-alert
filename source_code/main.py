import requests, time, requests, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

from utils import calculate_local_time
from weather_report import (
    kelvin_to_celcius_Fahrenheit, get_wind_direction, 
    beaufort_scale_calculation, assign_wind_condition,
    assign_storm_type, storm_alert
    )


def interval_weather_report(city_name, api, interval):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather?"
        current_directory = Path(__file__).resolve().parent 
        path_to_api = current_directory / api

        with open(path_to_api, 'r') as API:
            API_KEY = API.read().strip()

    except FileNotFoundError:
        print(f"Error: {api} not found in the directory: {current_directory}")
    except PermissionError:
        print(f"Error: Permission denied for the file: {path_to_api}")
    
    request_url = f"{url}appid={API_KEY}&q={city_name}"
    log_number = 1

    try:
        while True:
            try:
                response = requests.get(request_url).json()

                temp_kelvin = response['main']['temp']
                temp_celcius, temp_fahrenheit = kelvin_to_celcius_Fahrenheit(temp_kelvin)
                feels_like_temp_kelvin = response['main']['feels_like']
                feels_like_temp_celcius, feels_like_temp_fahrenheit = kelvin_to_celcius_Fahrenheit(feels_like_temp_kelvin)
                wind_speed = response['wind']['speed']
                wind_direction_degree = response['wind']['deg']
                wind_direction = get_wind_direction(wind_direction_degree)
                humidity = response['main']['humidity']
                pressure = response['main']['pressure']
                
                if 'wind' in response:
                    wind_gust = response['wind'].get('gust', 0)
                else: wind_gust= "N/A"

                if 'rain' in response:
                    rain_volume_1h = f"{response['rain'].get('1h', 0)} mm/h"
                else: rain_volume_1h = "N/A"

                description = response['weather'][0]['description']
                utc_shift_seconds = response['timezone']
                city = response['name']
                if city == "Turan": city = "Danang"
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sunrise_time = datetime.fromtimestamp(response['sys']['sunrise'], timezone.utc) + timedelta(seconds=response['timezone'])
                formatted_sunrise_time = sunrise_time.strftime("%Y-%m-%d %H:%M:%S")
                sunset_time = datetime.fromtimestamp(response['sys']['sunset'], timezone.utc) + timedelta(seconds=response['timezone'])
                formatted_sunset_time = sunset_time.strftime("%Y-%m-%d %H:%M:%S")

                local_time = calculate_local_time(utc_shift_seconds).strftime("%Y-%m-%d %H:%M:%S")

                wind_speed_beaufort_number, wind_gust_beaufort_number = beaufort_scale_calculation(wind_speed, wind_gust)


                print(f"LOG # {log_number} | CURRENT_TIME: {current_time}")
                print("-----------------------------------------------------")
                print(f"  Location: {city}") 
                print(f"Local time: {local_time}")
                print(f"   Sunrise: {formatted_sunrise_time}")
                print(f"    Sunset: {formatted_sunset_time}")
                print("-----------------------------------------------------")
                print(f"General weather: {description}")
                print(f"    Temperature: {temp_celcius:.2f}°C or {temp_fahrenheit:.2f}°F")
                print(f"     Feels like: {feels_like_temp_celcius:.2f}°C or {feels_like_temp_fahrenheit:.2f}°F")
                print(f"     Wind speed: {wind_speed} m/s >> burst {wind_gust} m/s")
                print(f" Wind direction: {wind_direction_degree}° ({wind_direction})")
                print(f"       Pressure: {pressure} hPa")
                print(f"       Humidity: {humidity} %")
                print(f"Rain volume for the past hour: {rain_volume_1h}")
                print("-----------------------------------------------------")
                print(f"Beaufort wind force: {wind_speed_beaufort_number} >> burst {wind_gust_beaufort_number}")

                storm_type = assign_storm_type(utc_shift_seconds)

                wind_speed_condition = assign_wind_condition(wind_speed_beaufort_number, storm_type)
                wind_gust_condition = assign_wind_condition(wind_gust_beaufort_number, storm_type)

                if wind_speed_condition == "None" and wind_gust_condition == "None":
                    pass
                else:
                    warning_message = ""

                    if wind_speed_condition != "None":
                        warning_message += f"{wind_speed_condition}"
                    if wind_gust_condition != "None":
                        if warning_message: # Checks if there is already a wind_speed_condition
                            warning_message += " >> "
                        warning_message += f"{wind_gust_condition}"
                    
                    if warning_message:
                        print(f"WARNING: {warning_message}")
                
                wait_time_offset = storm_alert(wind_speed_beaufort_number, wind_gust_beaufort_number)

                print("\n")
                log_number += 1
                time.sleep(interval - float(wait_time_offset))

            except KeyboardInterrupt:
                confirmation = input("Ending session. Would you like to restart? (y/n): ").strip().lower()
                if confirmation == "yes" or confirmation == "y":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                else:
                    break

    except Exception as e:
        print(f"Error: {e}.")


if __name__ == "__main__":
    city_name = str(input("Enter name of city: ")).strip()
    interval = int(input("Enter interval duration (seconds): "))

    os.system('cls' if os.name == 'nt' else 'clear')
    api = "api.txt"

    interval_weather_report(city_name, api, interval)