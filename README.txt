INTRODUCTION:
===========================
"Storm Alert" is a simple Python script that is primarily used to monitor storm severity for a specific city using Openweathermap. It is not meant for forecasting, but can be used to help track changes in weather data. These changes can occur due to shifts in temperature, pressure, wind speed, and often indicate the onset or occurrence of dynamic weather conditions.  

Moreover, please note that this script is mostly intended for detecting storm activity in cities within tropical or sub-tropical climates. The Beaufort Wind Force Scale is used to determine the severity of reported windspeed, and - depending on the assessed severity - will alert the user in the form of beeps.

For other weather events such as heat waves, cold fronts, or thunderstorms... These will have varying weather data depending on geography and climate, and often require an assessment of change over multiple reports. For now you may need to manually monitor these events. You can find references for this in the "weather_events.txt" file provided in the same folder. 

This is a personal project I've used to learn more about Python programming and API requests. Any feedbacks are welcome!


HOW TO USE:
===========================
1) SETUP:
-------------------
First, you will need an API key from OpenWeather (https://openweathermap.org). Make an account and retrieve your free API key. In the "storm_alert_{version number}" folder, you will see a folder named "_internal". Access this folder and find a text file called "api.txt", this is the file from which the script will extract your API key to request for weather data. Paste your API key into "api.txt" and save the file. 

2) RUNNING THE EXE:
-------------------
Everytime you run the script, you first will be prompted to enter a city name, and then the interval duration as presented below:

- "Enter name of city: " -> this is the name of the city in which the script will request weather data for. To be more precise, you can include a two-letter country code separated with a comma like so: "New York, US"

- "Enter interval duration (seconds): " -> The script will make report logs between intervals of your choice. For example, if you set the interval duration to be 60, then after the first report log, the script will make another report after every 60 seconds. To lessen repeating data - though this may vary depending on the location - it is recommended to set the interval duration to be at least 600 to 900 seconds (10 to 15 minutes).


A typical report log will have the following format:


LOG # _ | CURRENT_TIME: ____-__-__ __:__:__
-----------------------------------------------------
  Location: ______
Local time: ____-__-__ __:__:__
   Sunrise: ____-__-__ __:__:__
    Sunset: ____-__-__ __:__:__
-----------------------------------------------------
General weather: _____________
    Temperature: __.__°C or __.__°F
     Feels like: __.__°C or __.__°F
     Wind speed: _.__ m/s >> burst __.__ m/s
 Wind direction: ___° (_____)
       Pressure: ____ hPa
       Humidity: __ %
Rain volume for the past hour: ____ mm/h
-----------------------------------------------------
Beaufort wind force: _ >> burst _


- "LOG # n" -> Report log number, increments by one for each new log.
- "CURRENT_TIME" -> The time on the user's computer at the time of the current report.
- "Location" -> Name of the reported city.
- "Local time" -> Current time at the reported city. 
- "Sunrise" -> Time of sunrise at the reported city.
- "Sunset" -> Time of sunset at the reported city.
- "General weather" -> Overall description of the weather condition.
- "Temperature" -> The actual temperature, provided in both Celsius and Fahrenheit.
- "Feels like" -> What the temperature should 'feel like' in person. Accounts for humidity, atmospheric pressure, wind condition and other factors.
- "Wind speed" -> Sustained wind speed, usually over a 1-minute timespan. ">> burst" -> a sudden, intense increase in wind speed over a short period of time (usually a few seconds).
- "Wind direction" -> Direction where the wind blows from, starting at 0° (or 360°) for North and increases clockwise.
- "Pressure" -> Atmospheric pressure at sea level.
- "Humidity" -> Concentration of water vapor present in the air. It is a measure of how much moisture the air contains relative to the maximum amount it can hold at a given temperature. 
- "Rain volume for the past hour" -> How much rain that a square meter received in the last hour.
- "Beaufort wind force" -> an empirical measure that relates wind speed to observed conditions at sea or on land.


To break out of the report loop, press "Ctrl + C". The script will prompt you the following line:
"Ending session. Would you like to restart? (y/n): "

The script accepts "yes" or "y" (not case-sensitive) in which it will restart the loop with the current city and interval configurations. Otherwise, "no" or "n" will end the script instance.


3) STORM ALERT:
-------------------
In the case of a storm alert, the report log will have an extra line at the bottom as shown below:
"WARNING: ____ >> ____"

The warning accounts for both wind speed and wind gust. Positioning of the two warnings are reflective of the "Wind speed" row.

If either wind measurements fall within Beaufort wind force range[6, 10], the script will beep once.
If either wind measurements reach above Beaufort wind force 11, the script will beep twice.
If only one of two wind measurements fall within an alert range, then only the warning for that measurement will appear.

Examples:
- "WARNING: Strong Breeze >> Severe Gale" -> This indicates that the Beaufort wind force for 'wind speed' and 'wind gust' are 6 and 9, respectively -> The script will beep once.

- "WARNING: Storm >> Very Strong Typhoon" -> This indicates that the Beaufort wind force for 'wind speed' and 'wind gust' are 10 and 14, respectively -> The script will beep twice.

- "WARNING: Near Gale" -> In this case, only 'wind gust' falls within range[6, 10] -> The script will beep once.

Please note that typhoons and hurricanes have their own scale of measurement. This script only presents their equivalent measurement in the Beaufort scale. 


REFERENCES:
===========================
https://openweathermap.org
https://en.wikipedia.org/wiki/Beaufort_scale
https://en.wikipedia.org/wiki/Tropical_cyclone_scales
