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

translate_logger = logging.getLogger("TRANSLATOR")
translate_logger.setLevel(logging.INFO)
translate_handler = logging.FileHandler("translate.log")
translate_handler.setFormatter(formatter)
translate_logger.addHandler(translate_handler)
