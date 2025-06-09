from flask import Flask
from models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///family_tree.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    # Імпортуємо blueprint лише тут, після ініціалізації app і db
    from routes.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Якщо не використовуєш flask db migrate
    app.run(debug=True)
