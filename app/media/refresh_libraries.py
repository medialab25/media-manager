import requests
from requests.exceptions import RequestException

def refresh_libraries(jellyfin_url, jellyfin_token):
    return jellyfin_url, jellyfin_token