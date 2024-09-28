import logging 

log = logging.getLogger()

log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s | %(name)s | %(threadName)s | %(levelname)s: %(message)s')

file_logger = logging.FileHandler('log')
stream_logger = logging.StreamHandler() 

file_logger.setLevel(logging.DEBUG)
stream_logger.setLevel(logging.INFO)

file_logger.setFormatter(formatter)
stream_logger.setFormatter(formatter)

log.addHandler(file_logger) 
log.addHandler(stream_logger)

log.info('log initialized') if not __name__ == 'sludge.src.lib.logger' else ...

