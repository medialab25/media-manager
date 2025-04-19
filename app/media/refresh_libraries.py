import requests
from requests.exceptions import RequestException
import logging

# Refresh JellyFin libraries

def refresh_libraries(jellyfin_url, jellyfin_token):
    try:
        logging.info(f"Attempting to refresh JellyFin libraries at {jellyfin_url}")
        response = requests.post(
            f"{jellyfin_url}/Library/Refresh",
            headers={
                'X-MediaBrowser-Token': jellyfin_token,
                'Content-Type': 'application/json'
            },
            timeout=10  # Add timeout
        )
        
        logging.info(f"JellyFin API response status: {response.status_code}")
        logging.info(f"JellyFin API response text: {response.text}")
        
        if response.status_code in (200, 204):
            return {'status': 'ok', 'message': 'Successfully refreshed JellyFin libraries'}, 200
            
        return {
            'status': 'error',
            'message': f'JellyFin API error: {response.text}'
        }, response.status_code if response.status_code == 401 else 400
            
    except RequestException as e:
        logging.error(f"Failed to refresh libraries: {str(e)}")
        return {
            'status': 'error',
            'message': f'Failed to refresh libraries: {str(e)}'
        }, 500
