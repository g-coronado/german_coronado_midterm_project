from dataclasses import dataclass, field

@dataclass
class Player:
    first_name: str
    last_name: str
    position: str
    at_bats: int
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


@dataclass
class Lineup:
    players: list[Player] = field(default_factory=list)

    def add_player(self, player: Player):
        self.players.append(player)
    
    def remove_player(self, player: Player):
        self.players.remove(player)
    
    def move_player(self, player: Player, new_position: int):
        self.players.remove(player)
        self.players.insert(new_position, player)
    
    def edit_player_position(self, player: Player, new_position: str):
        player.position = new_position

    def edit_player_stats(self, player: Player, new_at_bats: int, new_hits: int):
        player.at_bats = new_at_bats
        player.hits = new_hits

    def retrieve_player(self, lineup_number: int):
        return self.players[lineup_number - 1]

    @property
    def number_of_players(self):
        return len(self.players)
    
    def __iter__(self):
        return iter(self.players)
    

