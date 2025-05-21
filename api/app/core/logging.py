import os
import logging

# Configure logging
logging = logging.getLogger(__name__)

# Create formatter
formatter = logging.Formatter(
    "%(levelname)s [%(name)s] [%(module)s:%(lineno)d] %(message)s"
)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add handler to logger
logging.addHandler(console_handler)
logging.setLevel(logging.INFO)
