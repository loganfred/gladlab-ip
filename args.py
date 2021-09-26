import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument('FILE')
parser.add_argument('-v', '--verbose', action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.WARNING)
