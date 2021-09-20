import json
import os
import sys
import csv
import re
import argparse
import logging
from datetime import date


def parseArgs(argv):
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
    parser.add_argument('-l', '--err_log',
                        action='store_true',
                        help='log the errors')

    args = parser.parse_args(argv)
    return args


def checkGenres(searchGenres, columnGenres):
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


def checkWithSearchParametersFilms(argumentsSearch, columns):
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


def parseLineMovies(line):
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


def do_map(id, line):
    """
    Map function for parse part of dataset

    Parameters
    __________
    id:   int   id of block
    line: list  list with elements of line

    Returns
    _______
    tuple
    """
    regex, yearFrom, yearTo, genres = json.loads(os.environ["CONDITIONS"])
    year, name, genresList = parseLineMovies(line)
    if checkWithSearchParametersFilms([regex, yearFrom, yearTo, genres], [year, name, genresList]):
        for genre in genresList:
            if genres:
                    if genre in genres:
                        yield genre, (name, year)
            else:
                yield genre, (name, year)
    else:
        raise ValueError("Bad movie")


def main(argv = None):

    args = parseArgs(argv)

    if args.err_log:
        logging.basicConfig(filename='logs.log', level=logging.ERROR)

    if args.genres:
        genres = args.genres.split("|")
    else:
        genres = None

    os.environ["CONDITIONS"] = json.dumps([args.regex, args.year_from, args.year_to, genres])
    
    try:
        data = sys.stdin.readlines()
    except IOError as e:
        if args.err_log:
            logging.error('Date: {0}. Error while reading csv data. Error: {1}'.format(date.today().strftime("%d/%m/%Y"), e))
        return 1

    reader = csv.reader(data)
    next(reader)

    try:
        for id, line in enumerate(reader):
            try:
                for key, value in do_map(id, line):
                    print('{0}\t("{1}",{2})'.format(key, value[0], value[1]))
            except ValueError:
                continue
    except Exception as e:
        if args.err_log:
            logging.error('Date: {0}. Error while parsing lines. Error: {1}'.format(date.today().strftime("%d/%m/%Y"), e))
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())