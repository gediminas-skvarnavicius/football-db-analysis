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
        self.home_players: dict
        self.away_players: dict
        self.away_player_pos: dict[int, tuple]
        self.home_player_pos: dict[int, tuple]

    class Player:
        def __init__(self, player_id):
            self.player_id: str = player_id
            self.attributes: dict

        def get_player_attributes(
            self, player_data: pd.DataFrame, date, player_id_name: str = "player_api_id"
        ):
            entries = player_data.loc[player_data[player_id_name] == self.player_id]
            entries_before_date = entries.loc[entries["date"] < date]
            latest_entry = (
                entries_before_date[
                    entries_before_date["date"] == entries_before_date["date"].max()
                ]
                .squeeze()
                .to_dict()
            )
            self.attributes = latest_entry

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
        # initiate empty dictionaries
        self.home_players = {}
        self.away_players = {}

        # Get home player column names and goalkeeper column names
        home_players_num = ["home_player_" + str(i) for i in np.arange(1, 12)]
        goaly_home_num = "home_player_" + str(
            next(key for key, val in self.home_player_pos.items() if val == (1, 1))
        )
        home_players_num.remove(goaly_home_num)

        # Get away player column names and goalkeeper column names
        away_players_num = ["away_player_" + str(i) for i in np.arange(1, 12)]
        goaly_away_num = "away_player_" + str(
            next(key for key, val in self.away_player_pos.items() if val == (1, 1))
        )
        away_players_num.remove(goaly_away_num)

        # Initiate a Player class with it's id for every home player and goalkeeper separately
        self.home_players["players"] = [
            self.Player(self.match_data[player]) for player in home_players_num
        ]
        self.home_players["goaly"] = self.Player(self.match_data[goaly_home_num])

        # Initiate a Player class with it's id for every away player and goalkeeper separately
        self.away_players["players"] = [
            self.Player(self.match_data[player]) for player in away_players_num
        ]
        self.away_players["goaly"] = self.Player(self.match_data[goaly_away_num])

    def calculate_attribute_difference(self, attribute):
        try:
            home_avg = sum(
                player.attributes[attribute] for player in self.home_players["players"]
            )
            away_avg = sum(
                player.attributes[attribute] for player in self.away_players["players"]
            )
            difference = home_avg - away_avg
            return difference
        except Exception:
            return np.nan

    def export_player_attributes(self, cols, how: str = "all"):
        atts = {}

        if how == "all":
            # Add home player attributes
            for i, player in enumerate(self.home_players["players"]):
                for col in cols:
                    atts[col + "_H_" + str(i + 1)] = player.attributes[col]
            for col in cols:
                atts[col + "_H_gk"] = self.home_players["goaly"].attributes[col]

            # Add away player attributes
            for i, player in enumerate(self.away_players["players"]):
                for col in cols:
                    atts[col + "_A_" + str(i + 1)] = player.attributes[col]
            for col in cols:
                atts[col + "_A_gk"] = self.away_players["goaly"].attributes[col]

        if how == "diff":
            # Add home player attributes
            for i, (player_h, player_a) in enumerate(
                zip(self.home_players["players"], self.away_players["players"])
            ):
                for col in cols:
                    try:
                        val = player_h.attributes[col] - player_a.attributes[col]
                    except:
                        val = np.nan
                    atts[col + "_dif_" + str(i + 1)] = val
            for col in cols:
                try:
                    val = (
                        self.home_players["goaly"].attributes[col]
                        - self.away_players["goaly"].attributes[col]
                    )
                except:
                    val = np.nan
                atts[col + "_dif_gk"] = val

        if how == "avg_diff":
            for col in cols:
                atts[col + "_avg_diff"] = self.calculate_attribute_difference(col) / 10
                try:
                    val = (
                        self.home_players["goaly"].attributes[col]
                        - self.away_players["goaly"].attributes[col]
                    )
                except:
                    val = np.nan
                atts[col + "_avg_diff_gk"] = val

        return atts


def outcome_guess_prob_diff(row, coef_a, coef_b):
    dif = row["win"] - row["loss"]
    if dif > coef_a:
        output = "Home Win"
    elif dif < -coef_b:
        output = "Home Loss"
    else:
        output = "Tie"
    return output


def classifier_train_prob_dif(params, prob_data, y_data):
    coef_a = params["coef_a"]
    coef_b = params["coef_b"]
    guess = prob_data.apply(outcome_guess_prob_diff, axis=1, args=(coef_a, coef_b))
    sum_false = ~(guess.values == y_data.values)
    return sum_false.astype(int)


def outcome_guess_prob_win(x: float, coef_win, coef_loss):
    """
    Assigns a match outcome value based on the probability of home team
    win by using two threshold coefficients.
    """
    if x >= 1 - coef_win:
        y = "Home Win"
    elif x <= coef_loss:
        y = "Home Loss"
    else:
        y = "Tie"
    return y


def classifier_train_prob_win(params, probs, y_data):
    """
    Calculates the match outcome based home win probabilities
    and given threshold coefficients.
    """
    coef_win = params["coef_win"]
    coef_loss = params["coef_loss"]
    guess = probs.apply(outcome_guess_prob_win, args=(coef_win, coef_loss))
    sum_false = ~(guess.values == y_data.values)
    return sum_false.astype(int)
