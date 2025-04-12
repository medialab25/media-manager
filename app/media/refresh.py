from flask import current_app, jsonify
import requests
from requests.exceptions import RequestException

def refresh():
    try:
        # Get JellyFin configuration from app config
        jellyfin_url = current_app.config['JELLYFIN']['URL']
        jellyfin_token = current_app.config['JELLYFIN']['TOKEN']
        
        # Prepare headers for JellyFin API request
        headers = {
            'X-Emby-Token': jellyfin_token,
            'Content-Type': 'application/json'
        }
        
        # Make POST request to JellyFin API
        response = requests.post(
            f"{jellyfin_url}/Library/Refresh",
            headers=headers
        )
        
        # Check response status
        if response.status_code == 200 or response.status_code == 204:
            return jsonify({
                'status': 'ok',
                'message': 'Successfully refreshed JellyFin libraries'
            })
        elif response.status_code == 401:
            return jsonify({
                'status': 'error',
                'message': 'Invalid JellyFin API token'
            }), 401
        else:
            return jsonify({
                'status': 'error',
                'message': f'JellyFin API error: {response.text}'
            }), 400
            
    except RequestException as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to connect to JellyFin server: {str(e)}'
        }), 500
    except KeyError as e:
        return jsonify({
            'status': 'error',
            'message': f'Missing JellyFin configuration: {str(e)}'
        }), 500
