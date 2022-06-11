"""Converting Telegram bot"""

import os

import telegram
from telegram.ext import \
    (Filters,
     MessageHandler,
     CommandHandler,
     ConversationHandler,
     Updater)
from telegram import \
    (ReplyKeyboardMarkup,
     KeyboardButton)
import tkinter as tk
from tkinter import filedialog
from threading import Thread
from datetime import datetime

from path_configures import convert_file
from save_data import save_data, show_stats
from localization import translate_to_language
from available_langs import LANGUAGES

# getting token and language for bot
token = os.environ.get('CBToken')
updater = Updater(token)
with open('language.txt', 'r') as f:
    language = f.read()

EXPECTED_LANG = 1

# buttons for extensions
extensions_buttons = [[KeyboardButton("PDF")], [KeyboardButton("JPEG")],
                      [KeyboardButton("TXT")], [KeyboardButton("BMP")],
                      [KeyboardButton("JPG")],
                      [KeyboardButton("CSV")], [KeyboardButton("MP3")],
                      [KeyboardButton("DOCX")], [KeyboardButton("MP4")],
                      [KeyboardButton("PNG")], [KeyboardButton("ICO")],
                      [KeyboardButton("DOC")], [KeyboardButton("TIFF")]]

# all available extensions
extensions = (".pdf", ".jpeg", ".txt", ".bmp",
              ".jpg", ".pptx", ".csv", ".mp3", ".docx",
              ".doc", ".mp4", ".png", ".ico", ".tiff")

# all available languages
languages = [[KeyboardButton(lang.title())] for lang in LANGUAGES.values()]


def get_lang_key(input_dict, value) -> str:
    """Getting key from LANGUAGES by value"""
    for key, val in input_dict.items():
        if value == val:
            return key
    return "No such a key"


def save_lang(lang: str) -> None:
    """Saves user's chosen language"""
    with open('language.txt', 'w') as file:
        file.write(lang)


def save_delete_data(file: str, name: str, message: str) -> None:
    """Deleting created file and then saving data into csv file."""
    os.remove(file)
    save_data(name, message, f'Sent document: {file}', datetime.now())


# uses filedialog from tkinter
def open_file() -> str:
    """Opens file in a new filedialog window"""
    return filedialog.askopenfilename(title="Select a File")


def start_bot(update, context) -> None:
    """starts bot"""
    chat = update.effective_chat
    user_name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id,
                             text=translate_to_language(f"Hello {user_name}, "
                                                        f"I'm a bot convertor.\n"
                                                        f"If you want to convert "
                                                        "any file, please choose a button "
                                                        "below."
                                                        "\nWrite /help for more info.", f"{language}"),
                             reply_markup=ReplyKeyboardMarkup(
                                 extensions_buttons))


def helper(update, context) -> None:
    """Return help manager for user"""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=translate_to_language("Click the button "
                                                                         "with the extension you "
                                                                         "want to get a new file. \n"
                                                                         "If you don't see "
                                                                         "statistics, "
                                                                         "open your browser.", language))


def show_statistics(update, context) -> None:
    """Shows statistics of user converting manipulations.
    Opens browser with histogram.
    """
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=translate_to_language(
        'Showing statistic...', language))
    show_stats()


def language_changing(update, context) -> int:
    """Begins a new conversation"""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=translate_to_language(
        'Please, select language', language), reply_markup=ReplyKeyboardMarkup(languages))
    return 1


def change_lang(update, context) -> int:
    """Changing language"""
    global language
    chat = update.effective_chat
    if update.message.text.lower() in LANGUAGES.values():
        language = get_lang_key(LANGUAGES, update.message.text.lower())
        context.bot.send_message(chat_id=chat.id, text=translate_to_language(
            "You've successfully changed language", language))
        save_lang(language)
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=chat.id, text=translate_to_language(
            "Unknown language",
            language))
        return ConversationHandler.END


def send_document(update, context) -> None:
    """Bot sends a file if input extension is valid"""
    chat = update.effective_chat
    if '.' + update.message.text.lower() in extensions:
        try:
            file = open_file()
            new_file = convert_file(file, '.' + update.message.text.lower())
            context.bot.send_document(chat_id=chat.id,
                                      document=open(new_file, 'rb'),
                                      filename=new_file,
                                      timeout=1000)['document']
            save_delete_data(new_file, update.message.chat.first_name,
                             update.message.text)
        except (FileNotFoundError, telegram.error.TimedOut):
            context.bot.send_message(chat_id=chat.id, text=translate_to_language("Couldn't convert this "
                                                                                 f"file to {update.message.text} 😥",
                                                                                 language))
    else:
        context.bot.send_message(chat_id=chat.id, text=translate_to_language("Unknown command 🤷‍♂️",
                                                                             language))


# creating a new conversation handler for changing language
conv_lang_handler = ConversationHandler(
    entry_points=[CommandHandler('language', language_changing)],
    states={
        EXPECTED_LANG: [MessageHandler(Filters.text, change_lang, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('start', start_bot), CommandHandler('help', helper),
               CommandHandler('stats', show_statistics)]
)


def filedialog_window() -> None:
    """Creates a looping tk window"""
    root = tk.Tk()
    root.withdraw()
    root.mainloop()


def server_start() -> None:
    """starts a server"""
    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_lang_handler)
    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(CommandHandler('help', helper))
    dispatcher.add_handler(CommandHandler('stats', show_statistics))
    dispatcher.add_handler(MessageHandler(Filters.all, send_document))
    updater.start_polling()


# we're creating two threads: one for tk window,
# another for bot`s server
if __name__ == '__main__':
    thread1 = Thread(target=filedialog_window)
    thread2 = Thread(target=server_start)
    thread1.start()
    thread2.start()
