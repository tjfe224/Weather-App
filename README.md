# Weather-App
This is an app I created as test of my coding skills given to me by Awesome Inc.
Included files
  •	weather.py: The source file
  •	weather.exe: The executable created with pyinstaller
  • state_codes.json:    
    o	Data file actually used
    o Lists the postal code of each United State as json so the program can interpret actual state or it's postal code
  •	city.list.json.gz, shorten_city_list.dat: Data files used for features I didn’t have time to implement
    o city.list.json.gz:
      * Lists all valid cities for the OpenWeather API
      * Due to ascii characters that are out of the range of readability for Python, this is opened as a gzip to avoid errors, then the valid json that's created is read
      * Obtained from openweather.org
      * Not used in code
    o shorten_city_list.dat:
      * same as above but only for cities in the United States
      * Not used in code

