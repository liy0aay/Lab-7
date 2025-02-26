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

    def get_air_quality(self):
        headers = {'x-api-key': AMBER_TOKEN}
        params = {'lat': self.lat, 'lng': self.lng}
        response = requests.get(self.base_url, headers=headers, params=params)
        response.raise_for_status()
        self.air_data = response.json()

    def format_report(self):
        station = self.air_data['stations'][0]
        current_time = datetime.now().strftime('%d.%m.%Y %H:%M')
        
        report = [
            f"{'-'*50}",
            "ДАННЫЕ О КАЧЕСТВЕ ВОЗДУХА В САНКТ-ПЕТЕРБУРГЕ",
            f"{'-'*50}",
            f"Актуально на: {current_time}",
            f"Координаты: {self.lat}, {self.lng}",
            ""
        ]
        
        if station.get('CO'):
            report.append(f"🔹 CO (угарный газ): {station['CO']} ppm")
        if station.get('NO2'):
            report.append(f"🔹 NO2 (диоксид азота): {station['NO2']} ppb")
        if station.get('OZONE'):
            report.append(f"🔹 O3 (озон): {station['OZONE']} ppb")
        if station.get('AQI'):
            category = station.get('aqiInfo', {}).get('category', '')
            report.append(f"🔹 Индекс AQI: {station['AQI']}" + 
                         (f" ({category})" if category else ""))

        return "\n".join(report)

    def show_results(self):
        report = self.format_report()
        print(report)
        
        #фрмирование уведомления
        notification = []
        station = self.air_data['stations'][0]
        
        if station.get('CO'):
            notification.append(f"CO (угарный газ): {station['CO']} ppm")
        if station.get('NO2'):
            notification.append(f"NO2 (диоксид азота): {station['NO2']} ppb")
        if station.get('OZONE'):
            notification.append(f"O3 (озон): {station['OZONE']} ppb")
        if station.get('AQI'):
            category = station.get('aqiInfo', {}).get('category', '')
            notification.append(f"AQI: {station['AQI']}" + 
                              (f" ({category})" if category else ""))

        if notification:
            if OS == 'Darwin':
                Notifier.notify("\n".join(notification), title="Качество воздуха")
            elif OS == 'Windows':
                ToastNotifier().show_toast(
                    "Качество воздуха",
                    "\r\n".join(notification),
                    duration=10
                )

if __name__ == '__main__':
    monitor = AirQualityMonitor()
    monitor.get_air_quality()
    monitor.show_results()