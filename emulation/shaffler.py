import logging
import sys
import argparse
from datetime import date
from typing import Optional, Sequence


def parseArgs(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reducers',
                        type=int,
                        default=1,
                        help="Count of reducers")
    parser.add_argument('-l', '--err_log',
                        action='store_true',
                        help='log the errors')

    args = parser.parse_args(argv)
    return args


def shuffle(numReducers: int = 1) -> list:
    """
    Shuffle function

    Parameters
    __________
    numReducers: int   number of reducers

    Returns
    _______
    tuple
    """
    shuffleItems = []

    prevKey = None
    values = []

    try:
        for line in sys.stdin:
            key, value = line.split("\t")
            if key != prevKey and prevKey != None:
                shuffleItems.append((prevKey, values))
                values = []
            prevKey = key
            values.append(value[:-1])
    except IOError as e:
        raise ValueError("Error while reding input. Error: {0}".format(e))
    finally:
        if prevKey != None:
            shuffleItems.append((key, values))

    result = []
    chunkSize = len(shuffleItems) / float(numReducers)
    last = 0.0

    while last < len(shuffleItems):
        result.append(shuffleItems[int(last):int(last + chunkSize)])
        last += chunkSize

    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parseArgs(argv)

    if args.err_log:
        logging.basicConfig(filename='logs.log', level=logging.ERROR)

    numberReducers = args.reducers
    try:
        for reducer in shuffle(numberReducers):
            for genre, movies in reducer:
                print("{0}\t[{1}]".format(genre, ','.join(map(str, movies))))
            print(' ')
    except ValueError as e:
        if args.err_log:
            logging.error('Date: {0}. Error while parsing lines. Error: {1}'.format(date.today().strftime("%d/%m/%Y"), e))
        return 1

    return 0


if __name__ == '__main__':
    exit(main())