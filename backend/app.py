from flask import Flask
from extensions import db
from blueprints import weight_bp, user_bp, password_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'VMBjKC2YDoXz66AAqnnlBQen'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    db.init_app(app)
    app.app_context().push()
    register_blueprints(app)
    
    return app

def register_blueprints(app):
    app.register_blueprint(user_bp.bp)
    app.register_blueprint(weight_bp.bp)
    app.register_blueprint(password_bp.bp)

if __name__ == '__main__':
    app = create_app()
    app.run() #host='0.0.0.0', port=5000, debug=True
