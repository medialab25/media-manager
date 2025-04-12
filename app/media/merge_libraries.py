import requests
from requests.exceptions import RequestException

def merge_libraries(jellyfin_url, jellyfin_token):
    try:
        response = requests.post(
            f"{jellyfin_url}/Library/Refresh",
            headers={
                'X-MediaBrowser-Token': jellyfin_token,
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code in (200, 204):
            return {'status': 'ok', 'message': 'Successfully refreshed JellyFin libraries'}
            
        return {
            'status': 'error',
            'message': f'JellyFin API error: {response.text}'
        }, response.status_code if response.status_code == 401 else 400
            
    except RequestException as e:
        return {
            'status': 'error',
            'message': f'Failed to refresh libraries: {str(e)}'
        }, 500
