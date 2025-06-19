class Player:
    def __init__(self, number, role, alive=True, death_type=None):
        self.number = number
        self.role = role
        self.alive = alive
        self.death_type = death_type
