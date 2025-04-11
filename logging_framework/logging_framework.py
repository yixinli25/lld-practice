from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
# import psycopg2

# 1. The logging framework should support different log levels, such as DEBUG, INFO, WARNING, ERROR, and FATAL.
# 2. It should allow logging messages with a timestamp, log level, and message content.
# 3. The framework should support multiple output destinations, such as console, file, and database.
# 4. It should provide a configuration mechanism to set the log level and output destination.
# 5. The logging framework should be thread-safe to handle concurrent logging from multiple threads.
# 6. It should be extensible to accommodate new log levels and output destinations in the future.

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5


class LogMessage:
    def __init__(self, level: LogLevel, message: str):
        self.level = level
        self.message = message
        self.timestamp = datetime.now()

    def get_level(self):
        return self.level
    
    def get_message(self):
        return self.message
    
    def get_timestamp(self):
        return self.timestamp
    
    def __str__(self):
        return f"[{self.level.name}] {self.timestamp} - {self.message}"
    

class LogAppender(ABC):
    @abstractmethod
    def append(self, log_message: LogMessage):
        pass


class FileAppender(LogAppender):
    def __init__(self, file_path):
        self.file_path = file_path

    def append(self, log_message: LogMessage):
        with open("./logging_framework/" + self.file_path, "a") as file:
            file.write(str(log_message) + "\n")


class DatabaseAppender(LogAppender):
    def __init__(self, db_url, username, password):
        self.db_url = db_url
        self.username = username
        self.password = password

    def append(self, log_message: LogMessage):
        try:

            print("DataBase Logic...")

            # connection = psycopg2.connect(self.db_url, self.username, self.password)
            # cursor = connection.cursor()
            # cursor.execute(
            #     "INSERT INTO logs (level, message, timestamp) VALUES (%s, %s, %s)",
            #     (log_message.get_level().name, log_message.get_message(), log_message.get_timestamp())
            # )
            # connection.commit()
            # cursor.close()
            # connection.close()
        except:
            print(f"Error when logging in database")


class ConsoleAppender(LogAppender):
    def append(self, log_message: LogMessage):
        print(log_message)


class LoggerConfig:
    def __init__(self, log_level: LogLevel, log_appender: LogAppender):
        self.log_level = log_level
        self.log_appender = log_appender

    def get_log_level(self):
        return self.log_level
    
    def set_log_level(self, log_level: LogLevel):
        self.log_level = log_level

    def get_log_appender(self):
        return self.log_appender
    
    def set_log_appender(self, log_appender: LogAppender):
        self.log_appender = log_appender


class Logger:
    _instance = None

    def __init__(self):
        if Logger._instance is not None:
            raise Exception("This class is a singleton!")
        
        Logger._instance = self
        self.config = LoggerConfig(LogLevel.INFO, ConsoleAppender())

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger()
        return Logger._instance
    
    def set_config(self, config: LoggerConfig):
        self.config = config

    def log(self, level: LogLevel, message: str):
        if level.value >= self.config.get_log_level().value:
            log_message = LogMessage(level, message)
            self.config.get_log_appender().append(log_message)

    def debug(self, message):
        self.log(LogLevel.DEBUG, message)

    def info(self, message):
        self.log(LogLevel.INFO, message)

    def warning(self, message):
        self.log(LogLevel.WARNING, message)

    def error(self, message):
        self.log(LogLevel.ERROR, message)

    def fatal(self, message):
        self.log(LogLevel.FATAL, message)


class LoggerDemo:

    @staticmethod
    def run():
        logger = Logger.get_instance()

        logger.info("This is an info message")
        logger.warning("This is an warning message")
        logger.error("This is an error message")

        config = LoggerConfig(LogLevel.DEBUG, FileAppender("app.log"))
        logger.set_config(config)

        logger.debug("This is a debug message")
        logger.info("This is an info message")

if __name__ == "__main__":
    LoggerDemo.run()