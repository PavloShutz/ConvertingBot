"""Converting Telegram bot"""

import os
from telegram.ext import Filters, MessageHandler, CommandHandler, Updater
from telegram import ReplyKeyboardMarkup, KeyboardButton
import tkinter as tk
from tkinter import filedialog
from threading import Thread
from datetime import datetime

from path_configures import convert_file
from save_data import save_data

with open('token.txt', 'r') as token_file:
    data = token_file.read()

updater = Updater(data)

extensions_buttons = [[KeyboardButton(".pdf")], [KeyboardButton(".jpeg")],
                      [KeyboardButton(".txt")], [KeyboardButton(".bmp")],
                      [KeyboardButton(".jpg")], [KeyboardButton(".pptx")],
                      [KeyboardButton(".bin")], [KeyboardButton(".csv")],
                      [KeyboardButton(".mp3")], [KeyboardButton(".docx")],
                      [KeyboardButton(".mp4")], [KeyboardButton(".png")],
                      [KeyboardButton(".ico")]]

buttons = (".pdf", ".jpeg", ".txt", ".bmp",
           ".jpg", ".pptx", ".bin", ".csv", ".mp3", ".docx",
           ".mp4", ".png", ".ico")


# uses filedialog from tkinter
def open_file():
    """Opens file in a new filedialog window"""
    return filedialog.askopenfilename(title="Select a File")


def start_bot(update, context):
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


def helper(update, context):
    """Return help manager for user"""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Click the button "
                                                   "with the extension you "
                                                   "want to get a new file")


def reply_message(update, context):
    """Bot sends a file if input is valid extension"""
    chat = update.effective_chat
    if update.message.text in buttons:
        try:
            file = open_file()
            new_file = convert_file(file, update.message.text)
            context.bot.send_document(chat_id=chat.id,
                                      document=open(new_file, 'rb'),
                                      filename=new_file,
                                      timeout=100)['document']
            os.remove(new_file)
            save_data(update.message.chat.first_name,
                      update.message.text,
                      f'Sent document: {new_file}', datetime.now())
        except FileNotFoundError:
            context.bot.send_message(chat_id=chat.id,
                                     text="Couldn't convert this "
                                          f"file to {update.message.text} 😥")
    else:
        context.bot.send_message(chat_id=chat.id, text="Unknown command 🤷‍♂️")


def dialog_window():
    """Creates a looping tk window"""
    root = tk.Tk()
    root.withdraw()
    root.mainloop()


def server_start():
    """starts a server"""
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(CommandHandler('help', helper))
    dispatcher.add_handler(MessageHandler(Filters.all, reply_message))
    updater.start_polling()


# we're creating two threads: one for tk window,
# another for bot`s server
if __name__ == '__main__':
    thread1 = Thread(target=dialog_window)
    thread2 = Thread(target=server_start)
    thread1.start()
    thread2.start()
