# run.py or manage.py
from app import create_app
from app.models import reset_db

app = create_app()

with app.app_context():
    if app.config.get("ENV") == "development":
        print("App is running in development mode.")
        reset_db()
    print("✔️ Database initialized with sample quests.")
