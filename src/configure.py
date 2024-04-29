import logging


def configure():
    '''
    Configures app.
    '''
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s:     [%(asctime)s] %(message)s',
                        datefmt="%d-%m-%Y %H:%M:%S")
