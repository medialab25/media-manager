from flask import Flask
import json
import os

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path) as f:
        config = json.load(f)
        print(f"Loaded configuration: {json.dumps(config, indent=2)}")
        app.config.update(config)
        
        # Ensure MEDIA_MERGE config is available
        if 'MEDIA_MERGE' not in app.config:
            raise ValueError("MEDIA_MERGE configuration not found in config.json")
    
    # Register blueprints
    from app.system import routes as system_routes
    from app.media import routes as media_routes
    
    app.register_blueprint(system_routes.bp)
    app.register_blueprint(media_routes.bp)
    
    return app

# Create app instance for Gunicorn
application = create_app() 