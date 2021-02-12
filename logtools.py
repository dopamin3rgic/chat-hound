import logging 

DEBUG = logging.DEBUG	
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR

def set_up_logging(name, level=INFO):
	logger = logging.getLogger(name)
	logger.setLevel(level)
	log_handler = logging.StreamHandler()
	logger.addHandler(log_handler)
	log_formatter = logging.Formatter("[%(levelname)s] %(filename)s: %(message)s")
	log_handler.setFormatter(log_formatter)
	return logger