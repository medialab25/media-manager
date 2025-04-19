from flask import Blueprint, jsonify, current_app
from app.media.refresh_libraries import refresh_libraries
from app.media.merge_libraries import merge_libraries

bp = Blueprint('media', __name__, url_prefix='/media')

def get_jellyfin_config():
    config = current_app.config['JELLYFIN']
    if not config.get('URL') or not config.get('TOKEN'):
        return None, {
            'status': 'error',
            'message': 'JellyFin configuration is missing URL or TOKEN'
        }
    return config, None

def get_merge_config():
    config = current_app.config['MEDIA_MERGE']
    return {
        'matrix': config['source_matrix'],
        'default_source': config['default_source_path'],
        'user_id': int(config['user']),
        'group_id': int(config['group'])
    }

def handle_merge():
    try:
        merge_config = get_merge_config()
        
        for media_type, type_config in merge_config['matrix'].items():
            source_paths = type_config.get('source_paths', [merge_config['default_source']])
            success = merge_libraries(
                media_type=media_type,
                source_paths=source_paths,
                quality_list=type_config['quality_order'],
                merged_path=type_config['merged_path'],
                user_id=merge_config['user_id'],
                group_id=merge_config['group_id']
            )
            if not success:
                return False, f'Failed to merge {media_type} libraries'
        
        return True, 'Successfully merged all libraries'
    except Exception as e:
        return False, f'Error during merge: {str(e)}'

@bp.route('/refresh', methods=['POST'])
def refresh():
    try:
        config, error = get_jellyfin_config()
        if error:
            return jsonify(error), 500
            
        result, status_code = refresh_libraries(config['URL'], config['TOKEN'])
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error during refresh: {str(e)}'
        }), 500

@bp.route('/merge', methods=['POST'])
def merge():
    success, message = handle_merge()
    status_code = 200 if success else 500
    return jsonify({
        'status': 'ok' if success else 'error',
        'message': message
    }), status_code

@bp.route('/merge_and_refresh', methods=['POST'])
def merge_and_refresh():
    success, message = handle_merge()
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 500
        
    try:
        config, error = get_jellyfin_config()
        if error:
            return jsonify(error), 500
            
        result, status_code = refresh_libraries(config['URL'], config['TOKEN'])
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error during refresh: {str(e)}'
        }), 500

@bp.route('/status')
def status():
    return jsonify({'message': 'Media status...'})
