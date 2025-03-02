"""Handles the database for the Greetings web site"""
import sqlite3
from typing import List, Tuple
import json

class QuestDB:

    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS teams
        (team TEXT NOT NULL UNIQUE,
        score INTEGER DEFAULT 1,
        the_answer INTEGER DEFAULT 0,
        git_monster INTEGER DEFAULT 0,
        the_gate INTEGER DEFAULT 0,
        the_crown INTEGER DEFAULT 0,
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
        try:
            cursor.execute(
                "INSERT INTO teams (team) VALUES (?);",
                (team,)
            )
            self._conn.commit()
            return cursor.lastrowid
        except:
            return False
        
    def get_team_as_json(self, team: str) -> str:
        team_data = self.get_team(team)
        if team_data:
            team_dict = {
                "team": team_data[0],
                "score": team_data[1],
                "the_answer": team_data[2],
                "git_monster": team_data[3],
                "the_gate": team_data[4],
                "the_crown": team_data[5],
                "date": team_data[6]
            }
            return json.dumps(team_dict)
        return json.dumps({})
        
    def get_team(self, team): #-> Tuple[int, str, str]:
        cur = self._conn.cursor()
        cur.execute(
            """SELECT *
                FROM teams
                WHERE team = ?;""",
            (team,),
        )
        return cur.fetchone()
    
    def update_level(self, team:str, level:str):
        levels = ['the_answer', 'git_monster', 'the_gate', 'the_crown']
        if level not in levels:
            print("invalid level")
            return (False, 'invalid level')
        
        team_json = self.get_team_as_json(team)
        if len(team_json) == 0:
            print("Team not found")
            return (False, 'Team not found')
        
        for i in range(levels.index(level)):
            if team_json[levels[i]] == 0:
                print(f"Previous level {levels[i]} not completed")
                return (False, f"Previous level {levels[i]} not completed")
            
        if team_json[level] == 1:
            print("Level already completed")
            return (False, 'Level already completed')
        
        cursor = self._conn.cursor()
        cursor.execute(
            f"UPDATE teams SET {level} = 1 WHERE team = ?;",
            (team,)
        )
        self._conn.commit()
        
        return True
    
    def update_score(self, team:str, deltaScore : int):
        if self.get_team(team):
            cursor = self._conn.cursor()
            cursor.execute(
                "UPDATE teams SET score = score + ? WHERE team = ?;",
                (deltaScore, team)
            )
            self._conn.commit()
            return True
        return False
    
    def all_teams(self) -> List[Tuple[int, str, int]]:
        cursor = self._conn.cursor()
        cursor.execute(
            """SELECT *
               FROM teams
               ORDER BY score DESC;"""
        )
        return cursor.fetchall()

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
