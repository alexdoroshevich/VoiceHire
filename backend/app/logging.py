"""Structlog configuration with API key scrubbing processor."""

import logging
import re

import structlog

# Patterns that match provider API keys -- redacted from all log output
_SECRET_PATTERNS = re.compile(
    r"(sk-ant-[a-zA-Z0-9\-_]+|sk-proj-[a-zA-Z0-9\-_]+|sk-[a-zA-Z0-9]{20,}"
    r"|dg_[a-zA-Z0-9\-_]+|el_[a-zA-Z0-9\-_]+"
    r"|retell_[a-zA-Z0-9\-_]+|rk_[a-zA-Z0-9\-_]+"
    r"|whsec_[a-zA-Z0-9\-_]+)",
    re.IGNORECASE,
)


def scrub_secrets(
    logger: structlog.types.WrappedLogger,
    method: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    """Redact API keys from log output."""
    for key, value in event_dict.items():
        if isinstance(value, str):
            event_dict[key] = _SECRET_PATTERNS.sub("[REDACTED]", value)
    return event_dict


def configure_logging() -> None:
    """Configure structlog with JSON output and secret scrubbing."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            scrub_secrets,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )
