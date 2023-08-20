from loguru import logger as logging

logging.add("logs/logs.log",
            rotation="500 MB",
            backtrace=True,
            diagnose=True,
            # pylint: disable=line-too-long
            format="<yellow>{time:YYYY-MM-DD at HH:mm:ss}</yellow> | <level>{level}</level>: <level>{message}</level>"
            # pylint: enable=line-too-long
            )
logging = logging.opt(colors=True)

