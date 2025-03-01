import requests
import platform
import webbrowser # позволяет открывать страницы в браузере
import os # для взаимодействия с файлами ос 
from datetime import datetime 

NASA_API_KEY = "WADFmQPvQE3J5nLjGil5UGSf9J8p2XdFlcjoondO"
OS = platform.system()

if OS == "Windows":
    from win10toast_click import ToastNotifier
elif OS == "Darwin":
    from pync import Notifier


class NASA_API:
    
    api_url = "https://api.nasa.gov/planetary/apod"

    def __init__(self, api_key=NASA_API_KEY):
        self.api_key = api_key
        self.data = None

    def request_apod(self):
        params = {
            "api_key": self.api_key
        }
        response = requests.get(self.api_url, params=params)
        self.data = response.json()
    
    def save_image(self):
    
        img_data = requests.get(self.data["url"]).content
        img_path = os.path.join(os.getcwd(), "nasa_apod.jpg")

        with open(img_path, "wb") as img_file:
            img_file.write(img_data)

        return img_path

    def show_console(self):
        
        title = self.data["title"]
        date = self.data["date"]
        explanation = self.data["explanation"]
        url = self.data["url"]

        print(f"Дата: {date}")
        print(f"Фото: {title}")
        print(f"Ссылка: {url}")
        print(f"Описание: {explanation}")

    def show_notification(self):
        if not self.data:
            return

        title = self.data["title"]
        explanation = self.data["explanation"][:100] + "..."  

        if OS == "Darwin":
            Notifier.notify(explanation, title=title, open=self.data["url"])

        elif OS == "Windows":
            img_path = self.save_image()
            toaster = ToastNotifier()
            toaster.show_toast(
                title, explanation,
                icon_path=img_path if img_path else None,  
                duration=10,
                callback_on_click=lambda: webbrowser.open(self.data["url"])
            )

    def open_photo(self):
        if not self.data:
            return
        
        url = self.data["url"]
        webbrowser.open(url)


if __name__ == "__main__":
    nasa_apod = NASA_API()
    nasa_apod.request_apod()
    nasa_apod.show_console()
    nasa_apod.show_notification()
    nasa_apod.open_photo()