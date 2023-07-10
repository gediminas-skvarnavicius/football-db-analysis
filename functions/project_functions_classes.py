import pandas as pd
from datetime import datetime
import numpy as np


class Team:
    """
    A class representing a team and its attribute entries.

    Attributes:
        id_code (int): The ID code of the team.
        attribute_entries (DataFrame): The attribute entries for the team.

    Methods:
        get_data(data: DataFrame, id_name: str = 'team_api_id') -> None:
            Retrieves and stores the attribute entries for the team from the given DataFrame.
    """

    def __init__(self, id_code):
        self.id_code = id_code
        self.attribute_entries: pd.DataFrame = None

    def get_data(self, data: pd.DataFrame, id_name="team_api_id"):
        """
        Retrieves and stores the attribute entries for the team from the given DataFrame.

        Args:
            data (DataFrame): The DataFrame containing the attribute entries.
            id_name (str, optional): The name of the ID column to filter the entries
            (default: 'team_api_id')

        Returns:
            None
        """
        self.attribute_entries = data.loc[data[id_name] == self.id_code]

    def get_latest_entry(
        self, date: str, cols: list[str], merge_id: str = "team_api_id"
    ) -> pd.DataFrame:
        """
        Returns the latest attribute entry before the specified date.

        Args:
            date (str): The date to compare against in "YYYY-MM-DD" format.

        Returns:
            DataFrame: The latest attribute entry before the specified date.

        """
        entries_before_date = self.attribute_entries[
            self.attribute_entries["date"] < date
        ]
        latest_entry = entries_before_date[
            entries_before_date["date"] == entries_before_date["date"].max()
        ][[merge_id] + cols].set_index(merge_id)

        if len(latest_entry) == 0:
            latest_entry = latest_entry.reindex([self.id_code])
        return latest_entry


class MatchPlayers:
    def __init__(self):
        self.match_data: dict = None
        self.home_player_ids: dict
        self.away_player_ids: dict
        self.away_player_pos: dict[int, tuple]
        self.home_player_pos: dict[int, tuple]

    def get_data(self, data: pd.DataFrame):
        self.match_data = data.to_dict()

    def get_player_positions(self):
        self.home_player_pos = {}
        self.away_player_pos = {}
        for i in np.arange(1, 12):
            self.home_player_pos[i] = (
                self.match_data["home_player_X" + str(i)],
                self.match_data["home_player_Y" + str(i)],
            )
            self.away_player_pos[i] = (
                self.match_data["away_player_X" + str(i)],
                self.match_data["away_player_Y" + str(i)],
            )

    def get_player_ids(self):
        self.home_player_ids = {}
        self.away_player_ids = {}

        home_players = ["home_player_" + str(i) for i in np.arange(1, 12)]
        goaly_home = "home_player_" + str(
            next(key for key, val in self.home_player_pos.items() if val == (1, 1))
        )
        home_players.remove(goaly_home)

        away_players = ["away_player_" + str(i) for i in np.arange(1, 12)]
        goaly_away = "away_player_" + str(
            next(key for key, val in self.away_player_pos.items() if val == (1, 1))
        )
        away_players.remove(goaly_away)

        self.home_player_ids["players"] = [
            self.match_data[player] for player in home_players
        ]
        self.home_player_ids["goaly"] = self.match_data[goaly_home]

        self.away_player_ids["players"] = [
            self.match_data[player] for player in away_players
        ]
        self.away_player_ids["goaly"] = self.match_data[goaly_away]
