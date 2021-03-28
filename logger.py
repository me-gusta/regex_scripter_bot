import logging.config

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": u'%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "txt": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": "log/regex_scripter.log",
            "mode": "a"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console", "txt"
        ]
    }
})

logger = logging.getLogger()
