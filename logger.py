import logging

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot_logger = logging.getLogger("BOT")
bot_logger.setLevel(logging.INFO)
bot_handler = logging.FileHandler("bot.log")
bot_handler.setFormatter(formatter)
bot_logger.addHandler(bot_handler)

scrapper_logger = logging.getLogger("SCRAPPER")
scrapper_logger.setLevel(logging.INFO)
scrapper_handler = logging.FileHandler("scrapper.log")
scrapper_handler.setFormatter(formatter)
scrapper_logger.addHandler(scrapper_handler)

server_logger = logging.getLogger("SERVER")
server_logger.setLevel(logging.INFO)
server_handler = logging.FileHandler("server.log")
server_handler.setFormatter(formatter)
server_logger.addHandler(server_handler)

translator_logger = logging.getLogger("TRANSLATOR")
translator_logger.setLevel(logging.INFO)
translator_handler = logging.FileHandler("translator.log")
translator_handler.setFormatter(formatter)
translator_logger.addHandler(translator_handler)
