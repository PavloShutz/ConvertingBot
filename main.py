"""Converting Telegram bot"""

import os as os
from telegram.ext import \
    (Filters,
     MessageHandler,
     CommandHandler,
     Updater)
from telegram import ReplyKeyboardMarkup, KeyboardButton
import tkinter as tk
from tkinter import filedialog
from threading import Thread
from datetime import datetime

from path_configures import convert_file
from save_data import save_data, show_stats

with open('token.txt', 'r') as token_file:
    data = token_file.read()

updater = Updater(data)

extensions_buttons = [[KeyboardButton("PDF")], [KeyboardButton("JPEG")],
                      [KeyboardButton("TXT")], [KeyboardButton("BMP")],
                      [KeyboardButton("JPG")], [KeyboardButton("PPTX")],
                      [KeyboardButton("CSV")], [KeyboardButton("MP3")],
                      [KeyboardButton("DOCX")], [KeyboardButton("MP4")],
                      [KeyboardButton("PNG")], [KeyboardButton("ICO")],
                      [KeyboardButton("DOC")], [KeyboardButton("TIFF")]]

buttons = (".pdf", ".jpeg", ".txt", ".bmp",
           ".jpg", ".pptx", ".csv", ".mp3", ".docx",
           ".doc", ".mp4", ".png", ".ico", ".tiff")


# uses filedialog from tkinter
def open_file() -> str:
    """Opens file in a new filedialog window"""
    return filedialog.askopenfilename(title="Select a File")


def start_bot(update, context) -> None:
    """This method starts bot"""
    chat = update.effective_chat
    user_name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id,
                             text=f"Hello {user_name}, "
                                  f"I'm a converting bot. "
                                  f"If you want to convert "
                                  "any file, please choose a button "
                                  "below."
                                  "\nWrite /help for more info.",
                             reply_markup=ReplyKeyboardMarkup(
                                 extensions_buttons))


def helper(update, context) -> None:
    """Return help manager for user"""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Click the button "
                                                   "with the extension you "
                                                   "want to get a new file.\n"
                                                   "If you don't see "
                                                   "statistics, "
                                                   "open your browser.")


def show_statistics(update, context) -> None:
    """Shows statistics of user converting manipulations.
    Opens browser with histogram.
    """
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Showing statistic...')
    show_stats()


def reply_message(update, context) -> None:
    """Bot sends a file if input is valid extension"""
    chat = update.effective_chat
    if '.' + update.message.text.lower() in buttons:
        try:
            file = open_file()
            new_file = convert_file(file, '.' + update.message.text.lower())
            context.bot.send_document(chat_id=chat.id,
                                      document=open(new_file, 'rb'),
                                      filename=new_file,
                                      timeout=1000)['document']
            os.remove(new_file)  # removes and saves data in csv file
            save_data(update.message.chat.first_name,
                      update.message.text,
                      f'Sent document: {new_file}', datetime.now())
        except FileNotFoundError:
            context.bot.send_message(chat_id=chat.id,
                                     text="Couldn't convert this "
                                          f"file to {update.message.text} 😥")
    else:
        context.bot.send_message(chat_id=chat.id, text="Unknown command 🤷‍♂️")


def dialog_window() -> None:
    """Creates a looping tk window"""
    root = tk.Tk()
    root.withdraw()
    root.mainloop()


def server_start() -> None:
    """starts a server"""
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(CommandHandler('help', helper))
    dispatcher.add_handler(CommandHandler('stats', show_statistics))
    dispatcher.add_handler(MessageHandler(Filters.all, reply_message))
    updater.start_polling()


# we're creating two threads: one for tk window,
# another for bot`s server
if __name__ == '__main__':
    thread1 = Thread(target=dialog_window)
    thread2 = Thread(target=server_start)
    thread1.start()
    thread2.start()
