from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    return app

db = SQLAlchemy()

if __name__ == '__main__':
    app = create_app()
    db = create_db(app)
    app.run(debug=True)
