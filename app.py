import os
# biblioteca panel para o desenvolvimento de aplicações web inteiramente em Python
import panel as pn
# biblioteca para interface com API do clima OpenWeatherMap
from pyowm import OWM
from pyowm.utils import config, timestamps

# carrega o template de estilos para os componentes da UI
pn.extension(template="fast")

# conecta com a API do clima, é importante ter a variável de ambiente OPENWEATHERMAP_API_KEY setada (criar conta é gratuito, e tem um limite de 100 requisições por dia)
open_weather_map = OWM(os.environ.get('OPENWEATHERMAP_API_KEY'))
manager = open_weather_map.weather_manager()

# template usado para formatar os resultados da API em um Markdown
weather_results_template = """## Detailed Status
{detailed_status}
## Wind
- speed: {wind_speed} m/s
- direction: {wind_direction} degrees
## Humidity
{humidity}%
"""

def check_weather(event: pn.param.param.Event):
    """Função que puxa alguns dos dados disponibilizados pela API do clima, formata eles no template definido acima, coloca como último elemento na coluna de componentes na UI, e torna o resultado visível."""
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

# input do nome da cidade
city_input = pn.widgets.TextInput(name="City", placeholder="Enter the city name here ...")

# input do nome do país
country_input = pn.widgets.TextInput(name="Country", placeholder="Enter the country name here ...")

# botão de confirmar dados do formulário
submit_button = pn.widgets.Button(name="Submit", on_click=check_weather)

# formulário
form = pn.WidgetBox(city_input, country_input, submit_button)

# coluna para mostrar os resultados
results = pn.Column("## Results", "")

# começa com a coluna dos resultados escondida
results.visible = False

# definição do layout da aplicação web
pn.Column("## Hello World!", form, results).servable()
