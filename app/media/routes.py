from flask import Blueprint, jsonify, current_app
from app.media.refresh import refresh_libraries

bp = Blueprint('media', __name__, url_prefix='/media')

@bp.route('/refresh')
def refresh():
    config = current_app.config['JELLYFIN']
    result, status_code = refresh_libraries(config['URL'], config['TOKEN'])
    return jsonify(result), status_code

@bp.route('/merge')
def merge():
    return jsonify({'message': 'Merging media...'})

@bp.route('/status')
def status():
    return jsonify({'message': 'Media status...'})
