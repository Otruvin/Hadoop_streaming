import os
import sys
import csv
import re
from typing import Optional, Sequence
import argparse
import logging
from datetime import date
import multiprocessing as mp
from functools import partial
import json


def parseArgs(argv: Optional[Sequence[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-reg', '--regex',
                        type=str,
                        help="Regular expression for search films by name")
    parser.add_argument('-yf', '--year_from',
                        type=int,
                        help="Oldest year release of selected films")
    parser.add_argument('-yt', '--year_to',
                        type=int,
                        help='Latest year release of selected films')
    parser.add_argument('-g', '--genres',
                        type=str,
                        help='Genres of films to search')
    parser.add_argument('-cp', '--count_processors',
                        type = int,
                        default=mp.cpu_count(),
                        help="Count of cpus for use")
    parser.add_argument('-cz', '--chunk_size',
                        type=int,
                        default=400,
                        help='Size for chunks to split input')
    parser.add_argument('-l', '--err_log',
                        action='store_true',
                        help='log the errors')

    args = parser.parse_args(argv)
    return args


def checkGenres(searchGenres: Optional[list], columnGenres: Optional[list]) -> bool:
    """
    check contains seraching genre in movie genres

    Parameters
    __________
    searchGenres: dict   search genres
    columnGenres: list   genres of movie

    Returns
    _______
    bool
    """
    if columnGenres == '(no genres listed)':
        return False

    if searchGenres is None:
        if columnGenres is None:
            return False
        return True

    if searchGenres and columnGenres:
        for genre in searchGenres:
            if genre in columnGenres:
                return True
    return False


def checkWithSearchParametersFilms(argumentsSearch: list, columns: list) -> bool:
    """
    Checking if the given search parameters for movies are met

    Parameters
    __________
    argumentsSearch: dict   search parameters
    columns:         list   columns from line

    Returns
    _______
    bool
    """
    regularExpr, yearFrom, yearTo, genreSearch = argumentsSearch
    year, title, genres = columns

    if year:
        if yearFrom and yearFrom > year:
            return False
        if yearTo and yearTo < year:
            return False
    else:
        return False
    if title:
        if regularExpr:
            if not bool(re.search(regularExpr, title)):
                return False
    else:
        return False

    return checkGenres(genreSearch, genres)


def parseLineMovies(line: list) -> tuple:
    """
    Parse line from movies

    Parameters
    __________
    line: list   line to parse

    Returns
    _______
    tuple
    """
    _, title, genre = line
    year = None
    matchYear = re.search(r"(?<=\()(\d{4})(?=\))", title)
    if matchYear:
        year = int(matchYear.group())
    if year is None:
        name = title
    else:
        matchName = re.search(r".+?(?= \(\d{4})", title)
        if matchName:
            name = matchName.group()
        else:
            name = None
    if re.search('[()]', genre):
        genresList = None
    else:
        genresList = genre.split("|")

    return year, name, genresList


def getMoviesFromCSV(chunkSize) -> list:
    """
    Get chunked data from input stream

    Returns
    _______
    list
    """
    try:
        result = []
        chunk = []
        for number, line in enumerate(sys.stdin):
            if number == 0:
                continue
            if (number % chunkSize == 0):
                result.append(chunk)
                chunk = []
            chunk.append(line)
        result.append(chunk)
    except IOError as e:
        raise ValueError("Error while reading data from console. Error: {0}".format(e))
    except Exception as e:
        raise ValueError("System error while reading input. Error: {0}".format(e))
    return result


def map(blockId: int, chunk: list) -> list:
    """
    Map function for parse part of dataset (single line)

    Parameters
    __________
    blockId:     int   id of part of dataset
    chunk:       list  list with elements of chunk
    conditions:  list  conditions for filtering moviess

    Returns
    _______
    list
    """
    regex, yearFrom, yearTo, genres = json.loads(os.environ["CONDITIONS"])
    result = []
    reader = csv.reader(chunk)
    for movie in reader:
        year, name, genresList = parseLineMovies(movie)
        if checkWithSearchParametersFilms([regex, yearFrom, yearTo, genres], [year, name, genresList]):
            for genre in genresList:
                if genres and genre in genres:
                    if genres:
                        if genre in genres:
                            result.append((genre, (name, year)))
                    else:
                        result.append((genre, (name, year)))
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:

    args = parseArgs(argv)

    if args.err_log:
        logging.basicConfig(filename='logs.log', level=logging.ERROR)

    if args.genres:
        genres = args.genres.split("|")
    else:
        genres = None

    os.environ["CONDITIONS"] = json.dumps([args.regex, args.year_from, args.year_to, genres])

    try:
        data = getMoviesFromCSV(args.chunk_size)
    except ValueError as e:
        if args.err_log:
            logging.error('Date: {0}. Error while reading csv data. Error: {1}'.format(date.today().strftime("%d/%m/%Y"), e))
        return 1

    with mp.Pool(args.count_processors - 1) as pool:
        mpMap = partial(map, 1)
        processedData = pool.map(mpMap, data)
        for processedChunk in processedData:
            for row in processedChunk:
                key, value = row
                print('{0}\t("{1}",{2})'.format(key, value[0], value[1]))
    
    return 0


if __name__ == '__main__':
    exit(main())