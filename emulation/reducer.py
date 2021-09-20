import argparse
import logging
import os
import re
import sys
from datetime import date
from typing import Optional, Sequence


def parseArgs(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-N',
                        type=int,
                        help="Regular expression for search films by name")
    parser.add_argument('-l', '--err_log',
                        action='store_true',
                        help='log the errors')

    args = parser.parse_args(argv)
    return args


def getChunkedData() -> list:
    """
    Get chunked data

    Returns
    _______
    list
    """
    data = []
    chunk = []
    try:
        for line in sys.stdin:
            if line == ' \n':
                data.append(chunk)
                chunk = []
            else:
                key, value = line.split("\t")
                values = re.split("(?<=\)),(?=\()", value)
                resultValues = []
                for value in values:
                    title = re.search('(?<=\(")(.*)(?=",)', value).group(0)
                    year = int(re.search('(?<=,)([\d]{4})(?=\))', value).group(0))
                    resultValues.append((title, year))
                chunk.append((key, resultValues))
    except IOError as e:
        raise ValueError("Error with input stream. Error: {0}".format(e))
    except Exception as e:
        raise ValueError("System error while reading data. Error: {0}".format(e))
    return data


def reduce(genre: str, movies: list) -> tuple:
    """
    Reduce function

    Parameters
    __________
    genre:  int   genre like key
    movies: tuple data with movies and border for output  

    Returns
    _______
    tuple
    """
    countRows = int(os.environ["COUNT_ROWS"])
    movies = sorted(movies, key=lambda movie: (-movie[1], movie[0]))
    if countRows != 0:
        if len(movies) > countRows:
            return (genre, movies[:countRows])
        else:
            return (genre, movies)
    else:
        return (genre, movies)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parseArgs(argv)

    if args.err_log:
        logging.basicConfig(filename='logs.log', level=logging.ERROR)
    
    try:
        data = getChunkedData()
    except ValueError as e:
        if args.err_log:
            logging.error('Date: {0}. Error while parsing lines. Error: {1}'.format(date.today().strftime("%d/%m/%Y"), e))
        return 1

    if args.N:
        os.environ["COUNT_ROWS"] = str(args.N)
    else:
        os.environ["COUNT_ROWS"] = '0'

    print("genre,title,year")
    for chunk in data:
        for key, values in chunk:
            resGenre, resMovieData = reduce(key, values)
            for movie in resMovieData:
                print('{0},"{1}",{2}'.format(resGenre, movie[0], movie[1]))

    return 0


if __name__ == '__main__':
    exit(main())
