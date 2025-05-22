import os
import logging as logging_module

# Configure logging
logger = logging_module.getLogger(__name__)

# Create formatter
formatter = logging_module.Formatter(
    "%(levelname)s [%(name)s] [%(module)s:%(lineno)d] %(message)s"
)

# Create console handler
console_handler = logging_module.StreamHandler()
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)
logger.setLevel(logging_module.INFO)

# Export logger as logging for backward compatibility
logging = logger
