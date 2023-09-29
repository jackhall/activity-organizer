from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import (
    Dict,
    List,
    Optional,
    Set,
)


@dataclass(frozen=True)
class User:
    name: str
    gender: str
    phone: str


@dataclass(frozen=True)
class GameOutcome:
    goals_for: Dict[User, int]
    goals_allowed: int


@dataclass
class Game:
    place: str
    time: datetime
    length: timedelta = timedelta(0, 5400, 0)  # 90 min
    outcome: Optional[GameOutcome] = None
    
    def __lt__(self, other) -> bool:
        ...


@dataclass(frozen=True)
class League:  # e.g. New Albany Soccer League
    name: str
    place: str
    fields: Set[str]
    length: timedelta
    team_fee: float
    player_fee: float
    num_players: int  # on each team
    min_women: int


@dataclass
class Group:  # e.g. Relegated Legends
    name: str
    players: Set[User]
    leagues: Set[League]
    stats: dict

    def register(self, 
        league: League,
        season: str,
        captain: User,
        players: Set[User],
    ) -> "Team":
        self.players |= players

        cost_per_player = (league.team_fee / len(players)) + league.player_fee
        balance_sheet = {
            user: cost_per_player for user in players
            if user in self.players
        }
        balance_sheet[captain] = 0.0
        return Team(self, league, season, captain, balance_sheet, [])


@dataclass
class Team:  # e.g. Relegated Legends A in Fall 2022
    group: Optional[Group]
    league: League
    season: str
    captain: User
    roster: Dict[User, float]
    schedule: List[Game]
    suffix: str = ""

    def schedule_game(self, field, dt: datetime):
        self.schedule.append(
            Game(self.league.place, dt, self.league.length)
        )
        self.schedule.sort()

    def cancel_game(self):
        ...

    def record_game(self, outcome: GameOutcome):
        ...

    @property
    def latest_game(self) -> Game:
        ...

    @property
    def next_game(self) -> Game:
        ...


def interact(interpret):
    active = True
    while active:
        text = input("}>")
        active = interpret(text)

    print("farewell")

