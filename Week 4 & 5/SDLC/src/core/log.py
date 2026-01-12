from contextvars import ContextVar
from enum import Enum
from pathlib import Path

import structlog
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_DIR = Path(__file__).parent
ENV_FILE = CURRENT_DIR / ".env"


class LogLevel(str, Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogSettings(BaseSettings):
    # LOGGING
    LOG_LEVEL: LogLevel = Field(validation_alias="LOG_LEVEL")

    # .env settings
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )


log_settings = LogSettings()


correlation_id: ContextVar[str] = ContextVar("correlation_id", default="N/A")


def add_context_processor(_, __, event_dict):
    # I can modify this to add more variable at the end of the logs
    # event_dict["random"] = "HI"
    event_dict["correlation_id"] = correlation_id.get()
    return event_dict


def setup_logging():
    log_level = log_settings.LOG_LEVEL

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
    return structlog.get_logger(name)


logger = get_logger(__name__)


def log_error(message: str) -> None:
    """
    Logs error message into errors.log file

    Args:
        message: error message to log
    """
    logger.error(message)
