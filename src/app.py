from configure import configure
import loop


def run():
    '''
    Entry app point.
    '''
    configure()
    loop._start()


if __name__ == '__main__':
    run()
