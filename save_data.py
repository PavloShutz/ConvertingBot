"""Module for saving data in csv file format"""

import csv

from plotly.graph_objs import Bar, Layout  # type: ignore
from plotly import offline  # type: ignore


file = 'data.csv'


def collect_data(filename: str) -> list:
    """Get file formats and their amount"""
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


def save_data(username, user_message, bot_message, time_added) -> None:
    """Appends a new data from bot"""
    with open(file, 'a') as csv_file:
        fieldnames = ['User', 'UserMessage', 'BotMessage',
                      'Time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'User': username, 'UserMessage': user_message,
                        'BotMessage': bot_message, 'Time': time_added})


def show_stats() -> None:
    """Shows a histogram"""
    y_values = [collect_data(file).count(i) for i in set(collect_data(file))]
    x_values = list(set(collect_data(file)))
    data = [Bar(x=x_values, y=y_values)]

    x_axis_config = {'title': 'File formats'}
    y_axis_config = {'title': 'Amount of converted formats'}
    layout = Layout(title='All converted formats',
                    xaxis=x_axis_config, yaxis=y_axis_config)
    offline.plot({'data': data, 'layout': layout}, filename='stats.html')
