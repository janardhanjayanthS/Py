import logging
import logging.handlers
import os
import sys
from contextvars import ContextVar

import structlog

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="N/A")


def add_context_processor(_, __, event_dict):
    event_dict["correlation_id"] = correlation_id.get()
    return event_dict


def setup_logging(log_file: str = "/var/log/samplebookapp/app.log"):
    # Used in foreign_pre_chain — does NOT include wrap_for_formatter
    foreign_processors = configure_foreign_processors()

    # Used in structlog.configure() — DOES include wrap_for_formatter at the end
    structlog_processors = foreign_processors + [
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    root_logger = logging.getLogger()
    root_logger.addHandler(get_console_handler(foreign_processors))

    # File handler only works on EC2/Linux; silently skip on Windows (local dev)
    try:
        root_logger.addHandler(get_file_handler(log_file, foreign_processors))
    except Exception:
        pass

    root_logger.setLevel(logging.INFO)

    structlog.configure(
        processors=structlog_processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def configure_foreign_processors() -> list:
    """
    Processors used for foreign (non-structlog) logs like uvicorn, sqlalchemy etc.
    wrap_for_formatter is intentionally excluded here — it belongs only in
    structlog.configure() as the final step for structlog's own pipeline.
    """
    return [
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
    ]


def get_console_handler(foreign_processors: list) -> logging.StreamHandler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer(),
            foreign_pre_chain=foreign_processors,
        )
    )
    return console_handler


def get_file_handler(
    log_file: str, foreign_processors: list
) -> logging.handlers.RotatingFileHandler:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=foreign_processors,
        )
    )
    return file_handler


def get_logger(name: str):
    return structlog.get_logger(name)
