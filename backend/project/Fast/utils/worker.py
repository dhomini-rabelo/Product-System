from decouple import config
import requests

def renew(browser_path):
    requests.get(f'http://localhost:8000/{browser_path}', headers={'renew': config('SECRET_KEY')})
