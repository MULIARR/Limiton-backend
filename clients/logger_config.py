import logging


class LoggerConfig:
    def __init__(self, name: str, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._configure_handler(level)
        self._disable_external_logs()

    def _configure_handler(self, level):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter('%(filename)-16s:%(lineno)-4d #%(levelname)-8s - %(name)-15s - %(message)s')
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    @staticmethod
    def _disable_external_logs():
        logging.getLogger('LiteClient').setLevel(logging.CRITICAL)

    def get_logger(self):
        return self.logger


app_logger_config = LoggerConfig(name='app_logger')
app_logger = app_logger_config.get_logger()

orders_logger_config = LoggerConfig(name='orders_logger')
orders_logger = app_logger_config.get_logger()

bot_logger_config = LoggerConfig(name='bot_logger')
bot_logger = app_logger_config.get_logger()

