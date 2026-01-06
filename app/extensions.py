from flask_sqlalchemy import SQLAlchemy
#from flask import g
#from db.db import UserDatabase

db: SQLAlchemy = SQLAlchemy()

# def get_db() -> UserDatabase:
#     """
#     Retrieves the GreetingsDB instance from the global context (g) 
#     or creates a new instance if it doesn't exist.

#     Returns:
#         GreetingsDB: The GreetingsDB instance.
#     """
#     db_instance = getattr(g, '_database', None)
#     if db_instance is None:
#         db_instance = g._database = UserDatabase()
#     return db_instance