from flask import Blueprint, jsonify
from app.media.refresh import refresh as refresh_libraries

bp = Blueprint('media', __name__, url_prefix='/media')

@bp.route('/refresh')
def refresh():
    return refresh_libraries()

@bp.route('/merge')
def merge():
    return jsonify({'message': 'Merging media...'})

@bp.route('/status')
def status():
    return jsonify({'message': 'Media status...'})
