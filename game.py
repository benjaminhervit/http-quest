class Game:
    levels = ['the_answer', 'git_monster', 'the_gate', 'the_crown']

    def level_is_valid(self, team_json, level):
        if level not in self.levels:
            print("invalid level")
            return (False, 'invalid level')
        
        team_json = db.get_team_as_json(team)
        if len(team_json) == 0:
            print("Team not found")
            return (False, 'Team not found')
        
        for i in range(self.levels.index(level)):
            if team_json[self.levels[i]] == 0:
                print(f"Previous level {self.levels[i]} not completed")
                return (False, f"Previous level {self.levels[i]} not completed")
            
        if team_json[level] == 1:
            print("Level already completed")
            return (False, 'Level already completed')
        
        return (True, 'Level is available')