"""Module for saving data in csv file format"""

import os
import csv
from datetime import datetime

from plotly.graph_objs import Bar, Layout  # type: ignore
from plotly import offline  # type: ignore


class DataManager:
    """Class implementing saving and managing csv data."""

    def __init__(self):
        self.file = 'data.csv'

    @staticmethod
    def __collect_data(filename: str) -> list:
        """Get file formats and their amount.
        Args:
            filename (str): filename to get extensions from.
        Returns:
            list of extensions.
        """
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader)
            file_extensions = []
            for row in reader:
                try:
                    file_extensions.append(row[1])
                except IndexError:
                    continue
        return file_extensions

    def save_delete_data(self, file: str,
                         user_name: str, message: str) -> None:
        """Deleting created file and then saving data into csv file.
        Args:
            file (str): file to save data in.
            user_name (str): user's name to save.
            message (str): user's message to save.
        """
        os.remove(file)
        self.__save_data(user_name, message,
                         f'Sent document: {file}', datetime.now())

    def __save_data(self, username: str, user_message: str,
                    bot_message: str, time_added: datetime) -> None:
        """Appends a new data from bot.
        Args:
            username (str): user's name to save.
            user_message (str): user's message to save.
            bot_message (str): bot`s reply message to save.
            time_added (datetime): time the bot sent message to save.
        """
        with open(self.file, 'a') as csv_file:
            fieldnames = ['User', 'UserMessage', 'BotMessage',
                          'Time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'User': username, 'UserMessage': user_message,
                            'BotMessage': bot_message, 'Time': time_added})

    def show_stats(self) -> None:
        """Shows a histogram in web-browser."""
        y_values = [self.__collect_data(self.file).count(i)
                    for i in set(self.__collect_data(self.file))]
        x_values = list(set(self.__collect_data(self.file)))
        data = [Bar(x=x_values, y=y_values)]

        x_axis_config = {'title': 'File formats'}
        y_axis_config = {'title': 'Amount of converted formats'}
        layout = Layout(title='All converted formats',
                        xaxis=x_axis_config, yaxis=y_axis_config)
        offline.plot({'data': data, 'layout': layout}, filename='stats.html')
