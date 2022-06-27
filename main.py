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

from path_configures import ConvertedFile
from save_data import DataManager
from localization import Localization
from available_langs import LANGUAGES


class BotConvertor:
    """A Bot Convertor class for Telegram-Desktop application."""

    def __init__(self):
        # setting token we can get from environ variable's value
        self.token = os.environ.get('CBToken')
        self.updater = Updater(self.token)
        self.language = self.__load_language('language.txt')
        self.EXPECTED_LANGUAGE = 1
        self.TIME_OUT = 1000  # time that bot can process sending message
        # end of conversation handler
        self.CONVERSATION_END = ConversationHandler.END
        # buttons for extensions
        self.extensions_buttons = \
            [[KeyboardButton("PDF")], [KeyboardButton("JPEG")],
             [KeyboardButton("TXT")], [KeyboardButton("BMP")],
             [KeyboardButton("JPG")],
             [KeyboardButton("CSV")], [KeyboardButton("MP3")],
             [KeyboardButton("DOCX")], [KeyboardButton("MP4")],
             [KeyboardButton("PNG")], [KeyboardButton("ICO")],
             [KeyboardButton("DOC")], [KeyboardButton("TIFF")]]
        # all available extensions
        self.extensions = (".pdf", ".jpeg", ".txt", ".bmp",
                           ".jpg", ".pptx", ".csv", ".mp3", ".docx",
                           ".doc", ".mp4", ".png", ".ico", ".tiff")

        # all available languages
        self.languages = [[KeyboardButton(language.title())]
                          for language in LANGUAGES.values()]

        self.conversation_language_handler = ConversationHandler(
            entry_points=[CommandHandler('language', self.language_changing)],
            states={
                self.EXPECTED_LANGUAGE:
                    [MessageHandler(Filters.text,
                                    self.change_language,
                                    pass_user_data=True)],
            },
            fallbacks=[CommandHandler('start', self.start_bot),
                       CommandHandler('help', self.helper),
                       CommandHandler('stats', self.show_statistics)],
        )

    @staticmethod
    def __load_language(filename: str) -> str:
        """Loading language from txt.
        Args:
            filename (str): the filename with language
        Returns:
            the language read from file
        """
        with open(filename, 'r') as f:
            return f.read()

    @staticmethod
    def __save_language(input_language: str) -> None:
        """Saves user's chosen language
        Args:
            input_language (str): the language to write into the 'language.txt'
        """
        with open('language.txt', 'w') as file:
            file.write(input_language)

    # uses filedialog from tkinter
    @staticmethod
    def open_file_for_converting() -> str:
        """Opens file in a new filedialog window.
        Returns:
            A filename with its absolute path. Returned files is always str.
        """
        return filedialog.askopenfilename(title="Select a File")

    def start_bot(self, update, context) -> None:
        """Starts bot"""
        chat = update.effective_chat
        user_name = update.message.chat.first_name
        context.bot.send_message(chat_id=chat.id,
                                 text=Localization().translate_to_language(
                                     f"Hello {user_name}, "
                                     f"I'm a bot convertor.\n"
                                     f"If you want to convert "
                                     "any file, please choose a button "
                                     "below."
                                     "\nWrite /help for more info.",
                                     f"{self.language}"),
                                 reply_markup=ReplyKeyboardMarkup(
                                     self.extensions_buttons))

    def helper(self, update, context) -> None:
        """Return help manager for user"""
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id,
                                 text=Localization().translate_to_language(
                                     "Click the button "
                                     "with the extension you "
                                     "want to get a new file. \n"
                                     "If you don't see "
                                     "statistics, "
                                     "open your browser.", self.language))

    def show_statistics(self, update, context) -> None:
        """Shows statistics of user converting manipulations.
        Opens browser with histogram.
        """
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id,
                                 text=Localization().translate_to_language(
                                     'Showing statistic...', self.language))
        DataManager().show_stats()

    def language_changing(self, update, context) -> int:
        """Begins a new conversation for changing user interface language
        Returns:
            state for conversation handler with code 1.
        """
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id,
                                 text=Localization().translate_to_language(
                                     'Please, select language', self.language),
                                 reply_markup=ReplyKeyboardMarkup(
                                     self.languages,
                                 ))
        return self.EXPECTED_LANGUAGE

    def change_language(self, update, context) -> int:
        """Changing language.
        Returns:
            The end of conversation with code 1.
        """
        chat = update.effective_chat
        if update.message.text.lower() in LANGUAGES.values():
            self.language = \
                Localization().get_language_key(LANGUAGES,
                                                update.message.text.lower())
            context.bot.send_message(chat_id=chat.id,
                                     text=Localization().translate_to_language(
                                         """You've successfully
                                         changed language""",
                                         self.language),
                                     reply_markup=ReplyKeyboardMarkup(
                                         self.extensions_buttons))
            self.__save_language(self.language)
            return self.CONVERSATION_END
        else:
            context.bot.send_message(chat_id=chat.id,
                                     text=Localization().translate_to_language(
                                         "Unknown language",
                                         self.language),
                                     reply_markup=ReplyKeyboardMarkup(
                                         self.extensions_buttons))
            return self.CONVERSATION_END

    def send_document(self, update, context) -> None:
        """Bot sends a file if input extension is valid.
        Returns:
            None
        """
        chat = update.effective_chat
        chosen_file_format = f'.{update.message.text.lower()}'
        if chosen_file_format in self.extensions:
            try:
                file = self.open_file_for_converting()
                new_file = ConvertedFile(file,
                                         chosen_file_format).convert_file()
                context.bot.send_document(chat_id=chat.id,
                                          document=open(new_file, 'rb'),
                                          filename=new_file,
                                          timeout=self.TIME_OUT)['document']
                DataManager().save_delete_data(new_file,
                                               update.message.chat.first_name,
                                               update.message.text)
            except (FileNotFoundError, telegram.error.TimedOut):
                context.bot.send_message(chat_id=chat.id,
                                         text=Localization().
                                         translate_to_language(
                                             f"Couldn't convert "
                                             f"this file to "
                                             f"{update.message.text} 😥",
                                             self.language))
        else:
            context.bot.send_message(chat_id=chat.id,
                                     text=Localization().translate_to_language(
                                         "Unknown command 🤷‍♂️",
                                         self.language))

    @staticmethod
    def filedialog_window() -> None:
        """Creates a looping tkinter window."""
        root = tk.Tk()
        root.withdraw()
        root.mainloop()

    def server_start(self) -> None:
        """Starts a server for telegram bot."""
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(self.conversation_language_handler)
        dispatcher.add_handler(CommandHandler('start', self.start_bot))
        dispatcher.add_handler(CommandHandler('help', self.helper))
        dispatcher.add_handler(CommandHandler('stats', self.show_statistics))
        dispatcher.add_handler(MessageHandler(Filters.all, self.send_document))
        self.updater.start_polling()


# we're creating two threads: one for tkinter window,
# another for bot`s server
if __name__ == '__main__':
    bot_convertor = BotConvertor()
    thread1 = Thread(target=bot_convertor.filedialog_window)
    thread2 = Thread(target=bot_convertor.server_start)
    thread1.start()
    thread2.start()
