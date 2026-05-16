import logging
from pythonjsonlogger import jsonlogger
import contextvars
from datetime import datetime

# Context variable to hold the correlation ID
correlation_id_ctx_var = contextvars.ContextVar("correlation_id", default=None)

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        correlation_id = correlation_id_ctx_var.get()
        if correlation_id:
            log_record['correlation_id'] = correlation_id

def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove all default handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logHandler = logging.StreamHandler()
    formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger

logger = logging.getLogger(__name__)
