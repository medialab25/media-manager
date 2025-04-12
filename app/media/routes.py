from flask import Blueprint, jsonify

bp = Blueprint('media', __name__, url_prefix='/media')

@bp.route('/refresh')
def refresh():
    return jsonify({'message': 'Refreshing media library...'})

@bp.route('/merge')
def merge():
    return jsonify({'message': 'Merging media...'})

@bp.route('/status')
def status():
    return jsonify({'message': 'Media status...'})
