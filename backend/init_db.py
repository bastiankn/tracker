from app import db, create_app

app = create_app()
db.drop_all()
db.create_all()