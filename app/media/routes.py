from flask import Blueprint, jsonify, current_app
from app.media.refresh_libraries import refresh_libraries
from app.media.merge_libraries import merge_libraries

bp = Blueprint('media', __name__, url_prefix='/media')

@bp.route('/refresh', methods=['POST'])
def refresh():
    try:
        config = current_app.config['JELLYFIN']
        if not config.get('URL') or not config.get('TOKEN'):
            return jsonify({
                'status': 'error',
                'message': 'JellyFin configuration is missing URL or TOKEN'
            }), 500
            
        result, status_code = refresh_libraries(config['URL'], config['TOKEN'])
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error during refresh: {str(e)}'
        }), 500

@bp.route('/merge', methods=['POST'])
def merge():
    try:
        config = current_app.config['MEDIA_MERGE']
        matrix = config['source_matrix']
        default_source = config['default_source_path']
        user_id = int(config['user'])
        group_id = int(config['group'])
        
        for media_type, type_config in matrix.items():
            source_paths = type_config.get('source_paths', [default_source])
            quality_list = type_config['quality_order']
            merged_path = type_config['merged_path']
            
            success = merge_libraries(
                media_type=media_type,
                source_paths=source_paths,
                quality_list=quality_list,
                merged_path=merged_path,
                user_id=user_id,
                group_id=group_id
            )
            if not success:
                return jsonify({
                    'status': 'error',
                    'message': f'Failed to merge {media_type} libraries'
                }), 500
        
        return jsonify({
            'status': 'ok',
            'message': 'Successfully merged all libraries'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error during merge: {str(e)}'
        }), 500

@bp.route('/merge_and_refresh', methods=['POST'])
def merge_and_refresh():
    try:
        config = current_app.config['MEDIA_MERGE']
        matrix = config['source_matrix']
        default_source = config['default_source_path']
        user_id = int(config['user'])
        group_id = int(config['group'])
        
        for media_type, type_config in matrix.items():
            source_paths = type_config.get('source_paths', [default_source])
            quality_list = type_config['quality_order']
            merged_path = type_config['merged_path']
            
            success = merge_libraries(
                media_type=media_type,
                source_paths=source_paths,
                quality_list=quality_list,
                merged_path=merged_path,
                user_id=user_id,
                group_id=group_id
            )
            if not success:
                return jsonify({
                    'status': 'error',
                    'message': f'Failed to merge {media_type} libraries'
                }), 500
        
        result, status_code = refresh_libraries(config['URL'], config['TOKEN'])
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error during merge: {str(e)}'
        }), 500

@bp.route('/status')
def status():
    return jsonify({'message': 'Media status...'})
