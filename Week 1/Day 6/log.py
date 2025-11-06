import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='errors.log',
    encoding='utf-8',
    level=logging.ERROR
)