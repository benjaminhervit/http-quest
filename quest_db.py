"""Handles the database for the Greetings web site"""
import sqlite3
from typing import List, Tuple
import json
import datetime

from game.level import LevelEnum as LE

class QuestDB:

    CREATE_SQL = f"""
    CREATE TABLE IF NOT EXISTS teams
        (team TEXT NOT NULL UNIQUE,
        exp INTEGER DEFAULT 1,
        {LE.REGISTRATION.value} INTEGER DEFAULT 0,
        {LE.THE_TEST.value} INTEGER DEFAULT 0,
        {LE.THE_MONSTER.value} INTEGER DEFAULT 0,
        {LE.THE_GATE.value} INTEGER DEFAULT 0,
        {LE.THE_THRONE_ROOM.value} INTEGER DEFAULT 0,
        {LE.THE_CROWN.value} INTEGER DEFAULT 0,
        date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
    """

    def __init__(self, db_name: str = "quest.db"):
        """
        Initializes the GreetingsDB object and creates the database and table 
        if not already created.

        Args:
            db_name (str, optional): The name of the database file. Defaults to "greetings.db".

        Doctests:
        >>> db = GreetingsDB(":memory:")
        >>> db.all_greetings()
        []
        >>> db.close()
        """
        self._db_name = db_name
        with sqlite3.connect(self._db_name,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            self._conn = conn
            cursor = self._conn.cursor()
            cursor.execute(self.CREATE_SQL)
            self._conn.commit()

    def store_team(self, team: str) -> int:
        cursor = self._conn.cursor()
        exists = self.get_team(team)
        if exists:
            return None
        try:
            cursor.execute(
                "INSERT INTO teams (team) VALUES (?);",
                (team,)
            )
            self._conn.commit()
            return cursor.lastrowid
        except:
            return None
    
    def convert_team_to_json(self, team_data: str) -> str:
        try:
            team_dict = {
                "team": team_data[0],
                "exp": team_data[1],
                LE.REGISTRATION.value : team_data[2],
                LE.THE_TEST.value : team_data[3],
                LE.THE_MONSTER.value : team_data[4],
                LE.THE_GATE.value : team_data[5],
                LE.THE_THRONE_ROOM.value : team_data[6],
                LE.THE_CROWN.value : team_data[7],
                "date": team_data[8].isoformat() if isinstance(team_data[8], (datetime.date, datetime.datetime)) else team_data[7]
            }
            return json.dumps(team_dict)
        except KeyError as e:
            return json.dumps({'error':str(e)})
    
    def get_team_as_json(self, team: str) -> str:
        team_data = self.get_team(team)
        if team_data:
            return self.convert_team_to_json(team_data)
        
    def get_team(self, team): #-> Tuple[int, str, str]:
        cur = self._conn.cursor()
        cur.execute(
            """SELECT *
                FROM teams
                WHERE team = ?;""",
            (team,),
        )
        return cur.fetchone()
    
    def get_level_status_from_team(self, team:str, level:str):
        if self.get_team(team):
            cursor = self._conn.cursor()
            cursor.execute(
                f"SELECT {level} FROM teams WHERE team = ?;",
                (team,)
            )
            return cursor.fetchone()[0]
        return None
    
    def update_level(self, team:str, level:str):
        if level not in [le.value for le in LE]:
            print(f"Invalid level name {level} sent to update_level in db")
            return None
        
        cursor = self._conn.cursor()
        cursor.execute(
            f"SELECT {level} FROM teams WHERE team = ?;",
            (team,)
        )
        
        level_status = cursor.fetchone()
        if level_status and level_status[0 ]== 1:
            print("level already updated")
            return None
        
        if not self.get_team(team):
            print(f"Team {team} not found. update_level() stopped.")
            return None
        
        cursor = self._conn.cursor()
        cursor.execute(
            f"UPDATE teams SET {level} = 1 WHERE team = ?;",
            (team,)
        )
        self._conn.commit()
        
        if cursor.rowcount > 0:
            print("Update level successful")
            return True
        else:
            print("Update level failed")
        return False
    
    def update_score(self, team:str, deltaScore : int):
        if self.get_team(team) is None:
            print(f"Invalid team name {team} send to update_level in db")
            return None
        
        cursor = self._conn.cursor()
        cursor.execute(
            "UPDATE teams SET exp = exp + ? WHERE team = ?;",
            (deltaScore, team)
        )
        self._conn.commit()
        return cursor.fetchone()
    
    def all_teams(self) -> List[Tuple[int, str, int]]:
        cursor = self._conn.cursor()
        cursor.execute(
            """SELECT *
               FROM teams
               ORDER BY exp DESC;"""
        )
        return cursor.fetchall()
    
    def all_teams_as_json(self):
        cursor = self._conn.cursor()
        cursor.execute(
            """SELECT *
               FROM teams
               ORDER BY exp DESC;"""
        )
        teams = cursor.fetchall()
        teams_json = [self.convert_team_to_json(team) for team in teams]
        return json.dumps(teams_json)
    
    # def delete_greeting(self, rowid: int) -> int:
    #     """
    #     Deletes a greeting from the database.

    #     Args:
    #         rowid (int): The row ID of the greeting to be deleted.

    #     Returns:
    #         int: The number of rows affected by the deletion.
    #     """

    #     cursor = self._conn.cursor()
    #     cursor.execute(
    #         "DELETE FROM greetings WHERE rowid = ?;",
    #         (rowid,)
    #     )
    #     self._conn.commit()
    #     return cursor.rowcount

    def close(self) -> None:
        """
        Closes the database connection.
        """
        self._conn.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
