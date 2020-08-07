__version__ = "0.1.0"

from .app import app
from pydantic import BaseModel

import asyncio
import logging
import logging.config

logging_config = {
    "version": 1,
    "formatters": {
        "pydantic_formatter": {
            "()": "kafkaesk.ext.logging.formatter.PydanticFormatter"
        },
    },
    "handlers": {
        "kafkaesk_handler": {
            "class": "kafkaesk.ext.logging.handler.PydanticKafkaeskHandler",
            "formatter": "pydantic_formatter",
            "app": "ext://kafkaesk_log_generator.app.app",
            "stream": "logs.kafkaesk_handler",
        },
        "stream_handler": {
            "class": "kafkaesk.ext.logging.handler.PydanticStreamHandler",
            "formatter": "pydantic_formatter",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "log_generator": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stream_handler", "kafkaesk_handler"],
        }
    },
}


class IndexLog(BaseModel):
    _is_log_model = True
    index: int


async def main():
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger("log_generator")

    async with app:
        index = 0
        while True:
            logger.info("Test Log", IndexLog(index=index))
            index += 1

            await asyncio.sleep(1)


def run():
    asyncio.run(main())


if __name__ == "__main__":

    asyncio.run(main())
