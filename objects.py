from dataclasses import dataclass, field

@dataclass
class Player:
    playerID: int
    batOrder: int
    firstName: str
    lastName: str
    position: str
    atBats: int
    hits: int


    @property
    def player_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def batting_average(self):
        if self.at_bats == 0:
            return format(0.0, '.3f')
        else:
            return format(round(self.hits / self.at_bats, 3), '.3f')

    