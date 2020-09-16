import os
import webbrowser
import time
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
url = 'http://127.0.0.1:8000/'
webbrowser.get(chrome_path).open(url)
time.sleep(5)
os.system("python manage.py runserver")

