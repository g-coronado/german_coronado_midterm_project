from dataclasses import dataclass

@dataclass
class Player:
    playerID: int | None = None
    batOrder: int = 0
    firstName: str = ''
    lastName: str = ''
    position: str = ''
    atBats: int = 0
    hits: int = 0


    @property
    def player_full_name(self):
        return f'{self.firstName} {self.lastName}'
    
    @property
    def batting_average(self):
        if self.atBats == 0:
            return format(0.0, '.3f')
        else:
            return format(round(self.hits / self.atBats, 3), '.3f')

    