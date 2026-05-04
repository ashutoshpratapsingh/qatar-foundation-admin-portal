from flask import Flask
from config import Config
from extensions import db, bcrypt, jwt
from flask_cors import CORS   # ✅ ADD THIS

from routes.auth_routes import auth_bp
from routes.opportunity_routes import opp_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)   # ✅ ADD THIS (important)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(opp_bp, url_prefix='/api/opportunities')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)