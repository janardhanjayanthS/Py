import logging
from contextvars import ContextVar

import structlog
from src.core.config import settings

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="N/A")


def add_context_processor(_, __, event_dict):
    event_dict["correlation_id"] = correlation_id.get()
    return event_dict


def setup_logging():
    log_level = settings.LOG_LEVEL 

    # Displayed in log console
    processors = [
        structlog.contextvars.merge_contextvars,
        add_context_processor,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
    ]

    processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    return structlog.get_logger(name)


logger = get_logger(__name__)


def log_error(message: str) -> None:
    """
    Logs error message into errors.log file

    Args:
        message: error message to log
    """
    logger.error(message)
