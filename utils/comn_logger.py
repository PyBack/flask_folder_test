import logging
import logging.handlers

# Set Default Formatter

formatter = logging.Formatter('%s(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Set My Logger

comn_logger = logging.getLogger('MY_FLASK_LOG')
comn_logger.setLevel(logging.DEBUG)
stream_log = logging.StreamHandler()
stream_log.setFormatter(formatter)
comn_logger.addHandler(stream_log)

# 로그 disabled
# comn_logger.disabled = True
