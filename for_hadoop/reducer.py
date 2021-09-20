import sys
import os
import argparse
import re
import logging


def parseArgs(argv = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-N',
                        type=int,
                        help="Regular expression for search films by name")
    parser.add_argument('-l', '--err_log',
                        action='store_true',
                        help='log the errors')

    args = parser.parse_args(argv)
    return args


def group():
    """
    Group function

    Returns
    _______
    list
    """
    group = []

    prevKey = None
    values = []

    try:
        for line in sys.stdin:
            key, value = line.split("\t")
            title = re.search('(?<=\(")(.*)(?=",)', value).group(0)
            year = int(re.search('(?<=,)([\d]{4})(?=\))', value).group(0))
            if key != prevKey and prevKey != None:
                group.append((prevKey, values))
                values = []
            prevKey = key
            values.append((title, year))
    except IOError as e:
        raise ValueError("Error with input stream. Error: {0}".format(e))
    except Exception as e:
        raise ValueError("System error while reading data. Error: {0}".format(e))
    finally:
        if prevKey != None:
            group.append((key, values))

    return group


def do_reduce(genre, movies):
    """
    Reduce function

    Parameters
    __________
    genre:     int   genre like key
    movies:    tuple data with movies and border for output 

    Returns
    _______
    tuple
    """
    countRows = int(os.environ["COUNT_ROWS"])
    movies = sorted(movies, key=lambda movie: (-movie[1], movie[0]))
    if countRows:
        if len(movies) > countRows:
            return (genre, movies[:countRows])
        else:
            return (genre, movies)
    else:
        return (genre, movies)


def main(argv = None):
    args = parseArgs(argv)

    if args.err_log:
        logging.basicConfig(filename='logs.log', level=logging.ERROR)
    
    try:
        data = group()
    except ValueError as e:
        if args.err_log:
            logging.error('Date: {0}. Error while parsing lines. Error: {1}'.format(date.today().strftime("%d/%m/%Y"), e))
        return 1

    if args.N:
        os.environ["COUNT_ROWS"] = str(args.N)
    else:
        os.environ["COUNT_ROWS"] = '0'

    print("genre,title,year")
    for key, values in data:
        resGenre, resMovieData = do_reduce(key, values)
        for movie in resMovieData:
            print('{0},"{1}",{2}'.format(resGenre, movie[0], movie[1]))

    return 0


if __name__ == '__main__':
    exit(main())