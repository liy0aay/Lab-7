import requests
import platform
from datetime import datetime

AMBER_TOKEN = "0142e3d1e1eccbc333050586b1ab603c0d69ec2dd432281c992b779ae60f7562"
OS = platform.system()

if OS == "Windows":
    from win10toast import ToastNotifier
elif OS == "Darwin":
    from pync import Notifier

class AirQualityMonitor:
    def __init__(self, lat=59.9343, lng=30.3351):
        self.base_url = "https://api.ambeedata.com/latest/by-lat-lng"
        self.lat = lat
        self.lng = lng
        self.air_data = None

    def fetch_air_quality(self):
        headers = {'x-api-key': AMBER_TOKEN}
        params = {'lat': self.lat, 'lng': self.lng}
        
        
        response = requests.get(self.base_url, headers=headers, params=params)
        response.raise_for_status()
        self.air_data = response.json()
     

    def format_report(self):
          
        station = self.air_data['stations'][0]
        current_time = datetime.now().strftime('%d.%m.%Y %H:%M')
        
        return (
            f"ДАННЫЕ О КАЧЕСТВЕ ВОЗДУХА\n"
            f"Актуально на: {current_time}\n"
            f"Координаты: {self.lat}, {self.lng}\n\n"
            f"CO (угарный газ): {station.get('CO', 'N/A')} ppm\n"
            f"NO2 (диоксид азота): {station.get('NO2', 'N/A')} ppb\n"
            f"O3 (озон): {station.get('OZONE', 'N/A')} ppb\n"
            f"Индекс AQI: {station.get('AQI', 'N/A')} "
        )

    def show_results(self):
        report = self.format_report()
        print(report)
        
        # Формируем уведомление
        station = self.air_data['stations'][0]
        message = (
            "CO (угарный газ): {co} ppm\n"
            "NO2 (диоксид азота): {no2} ppb\n"
            "O3 (озон): {o3} ppb\n"
            "Индекс AQI: {aqi} ({category})"
        ).format(
            co=station.get('CO', 'N/A'),
            no2=station.get('NO2', 'N/A'),
            o3=station.get('OZONE', 'N/A'),
            aqi=station.get('AQI', 'N/A'),
            category=station.get('aqiInfo', {}).get('category', 'N/A')
        )

        if OS == 'Darwin':
            Notifier.notify(
                message,
                title="ДАННЫЕ О КАЧЕСТВЕ ВОЗДУХА",
                sound="default"
            )
        elif OS == 'Windows':
            # Для Windows заменяем переносы строк
            message = message.replace('\n', '\r\n')
            ToastNotifier().show_toast(
                "ДАННЫЕ О КАЧЕСТВЕ ВОЗДУХА",
                message,
                duration=10
            )

if __name__ == '__main__':
    monitor = AirQualityMonitor()
    monitor.show_results()