"""Logging Configuration"""

import logging
import logging.config
import json
from pythonjsonlogger import jsonlogger
from backend.config import settings

# JSON logging format
class JSONFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(JSONFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

# Configure logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'json': {
            '()': JSONFormatter,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json' if settings.LOG_LEVEL == 'JSON' else 'standard',
            'level': settings.LOG_LEVEL,
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json' if settings.LOG_LEVEL == 'JSON' else 'standard',
            'level': settings.LOG_LEVEL,
        },
    },
    'root': {
        'level': settings.LOG_LEVEL,
        'handlers': ['console', 'file'],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
