from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="../frontend/dist", template_folder="../frontend/dist")
    CORS(app)
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    return app