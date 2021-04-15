from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import os
from antlr4 import *
from polybot.cl import *
from polybot import Config


def start(update, context):
    text = '''Hi! I'm a bot that allows to work with convex polygons.'''
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def handle_message(update, context):
    if 'polygons_dictionary' not in context.user_data:
        context.user_data['polygons_dictionary'] = {}
    try:
        program = update.message.text
        lexer = LanguageLexer(InputStream(program))
        token_stream = CommonTokenStream(lexer)
        parser = LanguageParser(token_stream)
        tree = parser.root()
        visitor = EvalVisitor(context.user_data['polygons_dictionary'])
        output, images_filenames = visitor.visit(tree)
        if output:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=output
            )
        for filename in images_filenames:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=open(filename, 'rb')
            )
            os.remove(filename)
    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣'
        )


def main():
    updater = Updater(token=Config.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()
