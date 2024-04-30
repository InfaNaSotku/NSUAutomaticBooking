from nsubooking.configure import configure
import nsubooking.loop as loop


__all__ = []


def run():
    '''
    Entry app point.
    '''
    configure()
    loop._start()
