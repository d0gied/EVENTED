from loguru import logger

logger.add("file_{time}.log", rotation="500 MB", level="DEBUG")
