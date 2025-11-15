from flask import Flask

def create_app():
    app = Flask(__name__)

    from .main import main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    return app
