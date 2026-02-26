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
    # I can modify this to add more variable at the end of the logs
    # event_dict["random"] = "HI"
    event_dict["correlation_id"] = correlation_id.get()
    return event_dict


def setup_logging():
    """Configure and initialize structured logging."""
    log_level = "INFO"

    # Displayed in log console
    processors = [
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

    # TO LOG AS JSON
    # processors.append(structlog.processors.JSONRenderer())
    # TO LOG IN CONSOLE
    processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    """Get a structured logger instance.

    Args:
        name: Logger name (typically __name__).

    Returns:
        Configured structlog logger instance.
    """
    return structlog.get_logger(name)
