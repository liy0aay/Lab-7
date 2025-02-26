import requests  # выполнять HTTP-запросы
import platform  # определяет ОС

TOKEN = "6900144b4ab026e0e19a72ff1f36ab0a"
OS = platform.system()  # получает строку с названием ОС (macOS - это Darwin)

if OS == "Windows":
    from win10toast import ToastNotifier
elif OS == "Darwin":
    from pync import Notifier


class WeatherAPI:

    token = ''
    base_url = "http://api.openweathermap.org"
    coord_url = '/geo/1.0/direct'
    weather_url = '/data/2.5/weather'

    def __init__(self, city='Saint-Petersburg', country='Russia', lg='ru'):
        self.city = city
        self.country = country
        self.language = lg
        self.token = WeatherAPI.token  

    def request_details(self):
        params = {
            'q': f'{self.city},{self.country}',
            'limit': 1,
            'appid': self.token
        }
        url = f'{self.base_url}{self.coord_url}'
        details = requests.get(url, params=params)
        
        data = details.json()[0]
        self.retrieve_coordinates(data)

    def retrieve_coordinates(self, data):
        self.lat = data['lat']
        self.lon = data['lon']

    def request_weather(self):
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'units': 'metric',
            'appid': self.token,
            'lang': self.language
        }
        url = f'{self.base_url}{self.weather_url}'
        weather = requests.get(url, params=params)

        if weather.status_code != 200 or not weather.json():  # Проверка наличия данных
            print("Ошибка получения данных о погоде!")
            return

        self.weather = weather.json()

    def string_weather(self):
       
        city = self.weather['name']
        temp = self.weather['main']['temp']
        humidity = self.weather['main']['humidity']
        pressure = self.weather['main']['pressure']
        weather = self.weather['weather'][0]
        details = weather['description'].capitalize()
        return f'{city} {temp}°C\n{details}\nВлажность: {humidity}%\nДавление: {pressure} гПа'
   
    def show(self):
        data = self.string_weather().split('\n')
        title, details = data[0], "\n".join(data[1:])

        if OS == 'Darwin':
            Notifier.notify(details, title=title)
        elif OS == 'Windows':
            toaster = ToastNotifier()
            toaster.show_toast(title, details, duration=10)

    def show_console(self):
        print(self.string_weather())


if __name__ == '__main__':
    WeatherAPI.token = TOKEN
    weather = WeatherAPI()
    weather.request_details()
    weather.request_weather()
    weather.show_console()
    weather.show()