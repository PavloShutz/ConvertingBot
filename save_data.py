"""Module for saving data in csv file format"""

import csv


def save_data(username, user_message, bot_message, time_added) -> None:
    """Appends a new data from bot"""
    with open('data.csv', 'a') as csv_file:
        fieldnames = ['User', 'UserMessage', 'BotMessage',
                      'Time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'User': username, 'UserMessage': user_message,
                        'BotMessage': bot_message, 'Time': time_added})
