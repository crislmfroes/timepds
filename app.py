import os
import panel as pn
from pyowm import OWM
from pyowm.utils import config, timestamps

pn.extension(template="fast")

open_weather_map = OWM(os.environ.get('OPENWEATHERMAP_API_KEY'))
manager = open_weather_map.weather_manager()

weather_results_template = """## Detailed Status
{detailed_status}
## Wind
- speed: {wind_speed} m/s
- direction: {wind_direction} degrees
## Humidity
{humidity}%
"""

def check_weather(event: pn.param.param.Event):
    results.visible = False
    observation = manager.weather_at_place(f"{city_input.value},{country_input.value}")
    weather = observation.weather
    wind = weather.wind()
    results[-1] = weather_results_template.format(
        detailed_status=weather.detailed_status,
        wind_speed=wind['speed'],
        wind_direction=wind['deg'],
        humidity=weather.humidity
    )
    results.visible = True

city_input = pn.widgets.TextInput(name="City", placeholder="Enter the city name here ...")
country_input = pn.widgets.TextInput(name="Country", placeholder="Enter the country name here ...")
submit_button = pn.widgets.Button(name="Submit", on_click=check_weather)

form = pn.WidgetBox(city_input, country_input, submit_button)

results = pn.Column("## Results", "")
results.visible = False

pn.Column("## Hello World!", form, results).servable()