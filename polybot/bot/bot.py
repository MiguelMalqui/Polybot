from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, CallbackContext
import telegram
import os
from antlr4 import *
from polybot.cl import *
from polybot import Config


async def start(update: telegram.Update, context: CallbackContext):
    await update.message.reply_text(
        text='Hi! I\'m a bot that allows to work with convex polygons.',
    )


async def handle_message(update: telegram.Update, context: CallbackContext):
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
            await update.message.reply_text(
                text=output
            )
        for filename in images_filenames:
            with open(filename, 'rb') as f:
                await update.message.reply_photo(
                    photo=f,
                    caption=f'Image: {filename}'
                )
            os.remove(filename)
    except Exception as e:
        print(e)
        await update.message.reply_text(
            text='An error occurred while processing your request. Please check your input and try again.'
        )


def main():
    application = ApplicationBuilder().token(Config.TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
