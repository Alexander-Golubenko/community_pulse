from flask import Flask
from app.routers.questions import questions_bp
from app.routers.response import response_bp
from app.routers.categories import categories_bp
from config import DevelopmentConfig
from app.models import db
from flask_migrate import Migrate

def create_app():

    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)
    app.register_blueprint(categories_bp)

    @app.route('/')
    def index():
        return '<h3>Добро пожаловать в Community Pulse API</h3>' \
               '<p>Доступные endpoints: <br>' \
               '<a href="/questions/">/questions/</a> — работа с вопросами<br>' \
               '<a href="/response/">/response/</a> — ответы и статистика</p>'

    return app
