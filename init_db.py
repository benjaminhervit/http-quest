# init_db.py
from app import create_app
from app.models import reset_db

app = create_app()
with app.app_context():
    reset_db()
    print("DB reset done.")
