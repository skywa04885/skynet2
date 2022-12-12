import sys
import logging

from gui.application import Application

LOG_FORMAT = (
    '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) ''-35s %(lineno) -5d: %(message)s')


def main() -> None:
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    application = Application()
    application.run(sys.argv)


if __name__ == '__main__':
    main()
