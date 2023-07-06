import pandas as pd
from datetime import datetime


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
