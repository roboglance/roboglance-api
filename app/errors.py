class NonexistentTeamError(Exception):
    def __init__(self, team_number: int):
        super().__init__(f"Team number {team_number} not found.")
