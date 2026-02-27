import logging
import logging.handlers
import os
import sys
from contextvars import ContextVar

import structlog

# correlation_id is unique for each req, tracks it
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="N/A")


def add_context_processor(_, __, event_dict):
    """Add correlation ID to log events.

    Args:
        _: Logger name (unused).
        __: Method name (unused).
        event_dict: Event dictionary to modify.

    Returns:
        Modified event dictionary with correlation ID.
    """
    event_dict["correlation_id"] = correlation_id.get()
    return event_dict


def setup_logging(log_file: str = "/var/log/myapp/app.log"):
    log_level = "INFO"
    shared_processors = configure_shared_processor()

    # --- Attach both handlers to the root logger ---
    root_logger = logging.getLogger()
    root_logger.addHandler(get_console_handler(shared_processors=shared_processors))
    root_logger.addHandler(
        get_file_handler(log_file=log_file, shared_processors=shared_processors)
    )
    root_logger.setLevel(log_level)

    # --- Configure structlog to use stdlib as its backend ---
    structlog.configure(
        processors=shared_processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.stdlib.LoggerFactory(),  # <-- key change
        cache_logger_on_first_use=True,
    )


def configure_shared_processor() -> list:
    # --- Shared pre-processors (run before rendering) ---
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        add_context_processor,
        structlog.processors.add_log_level,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.PATHNAME,
            }
        ),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        # This bridges structlog events into stdlib logging
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]
    return shared_processors


def get_console_handler(shared_processors: list) -> logging.StreamHandler:
    # --- Console handler: human-readable colored output ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer(),
            foreign_pre_chain=shared_processors,
        )
    )
    return console_handler


def get_file_handler(
    log_file: str, shared_processors: list
) -> logging.handlers.RotatingFileHandler:
    # --- File handler: JSON output, rotates at 10MB, keeps 5 backups ---
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=shared_processors,
        )
    )
    return file_handler


def get_logger(name: str):
    """Get a structured logger instance.

    Args:
        name: Logger name (typically __name__).

    Returns:
        Configured structlog logger instance.
    """
    return structlog.get_logger(name)
