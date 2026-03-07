from dataclasses import dataclass

@dataclass
class Player:
    """
    Represents a baseball player with identifying information and basic
    batting statistics.

    Attributes
    ----------
    playerID : int | None
        Unique identifier for the player. May be None for unsaved players.
    batOrder : int
        Batting order position in the lineup (1–9).
    firstName : str
        Player's given name.
    lastName : str
        Player's family name.
    position : str
        Defensive position abbreviation (e.g., '1B', 'SS', 'CF').
    atBats : int
        Total number of official at-bats.
    hits : int
        Total number of recorded hits.
    """

    playerID: int | None = None
    batOrder: int = 0
    firstName: str = ''
    lastName: str = ''
    position: str = ''
    atBats: int = 0
    hits: int = 0
    

    @property
    def player_full_name(self) -> str:
        """
        Returns the player's full name.

        Returns
        -------
        str
            A string combining first and last name.
        """
        return f'{self.firstName} {self.lastName}'
    
    @property
    def batting_average(self) -> str:
        """
        Calculates the player's batting average formatted to three decimals.

        The batting average is computed as:
            hits / atBats
        If the player has zero at-bats, the result defaults to 0.000.

        Returns
        -------
        str
            Batting average formatted as a three-decimal string (e.g., '0.286').
        """
        if self.atBats == 0:
            return format(0.0, '.3f')
        else:
            return format(round(self.hits / self.atBats, 3), '.3f')
        