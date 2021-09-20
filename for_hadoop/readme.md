# Top movies by genres

The script allows user to get a list of movies sorted and filtered by conditions that entered was entered.

### Syntax for using the script

    ./get-movies.sh [args for search]

### Usage

### Help command

`-h | --help` - Show help message.

Example of using command:

    ./get-movies.sh --help

It returns:

    usage: mapper.py [-h] [-reg REGEX] [-yf YEAR_FROM] [-yt YEAR_TO] [-g GENRES] [-l]

    optional arguments:
    -h, --help            show this help message and exit
    -reg REGEX, --regex REGEX
                            Regular expression for search films by name
    -yf YEAR_FROM, --year_from YEAR_FROM
                            Oldest year release of selected films
    -yt YEAR_TO, --year_to YEAR_TO
                            Latest year release of selected films
    -g GENRES, --genres GENRES
                            Genres of films to search
    -l, --err_log         log the errors
    usage: reducer.py [-h] [-N N] [-l]

    optional arguments:
    -h, --help     show this help message and exit
    -N N           Regular expression for search films by name
    -l, --err_log  log the errors

### Get all movies

Example of using command:
    
    ./get-movies.sh

It returns:

    genre,title,year
    Action,"Ant-Man and the Wasp",2018
    Action,"Avengers: Infinity War - Part I",2018
    Action,"Bungo Stray Dogs: Dead Apple",2018
    Action,"Deadpool 2",2018
    Action,"Death Wish",2018
    Action,"Game Night",2018
    Action,"Game Over, Man!",2018
    Action,"Incredibles 2",2018
    Action,"Jurassic World: Fallen Kingdom",2018
    Action,"Maze Runner: The Death Cure",2018
    Action,"Mission: Impossible - Fallout",2018
    Action,"Pacific Rim: Uprising",2018
    Action,"Rampage",2018
    Action,"Solo: A Star Wars Story",2018
    Action,"SuperFly",2018
    Action,"Tomb Raider",2018
    Action,"Alien: Covenant",2017
    Action,"Baby Driver",2017
    Action,"Baywatch",2017
    Action,"Black Butler: Book of the Atlantic",2017
    Action,"Black Panther",2017
    Action,"Bright",2017
    Action,"CHiPS",2017
    Action,"Captain Underpants: The First Epic Movie",2017
    Action,"Dunkirk",2017
    Action,"Free Fire",2017
    Action,"Fullmetal Alchemist 2018",2017
    Action,"Geostorm",2017
    
    ...

### Add results to csv

Example of using the command:

    ./get-movies.sh > AllMoviesRates.csv

This command will create a `AllMoviesRates.csv` file.

### Get N films by all genres

`-N <count of films>` - Number of selectable films.

Example of using the command:

    ./get-movies.sh -N 3

It returns:

    genre,title,year
    Action,"Ant-Man and the Wasp",2018
    Action,"Avengers: Infinity War - Part I",2018
    Action,"Bungo Stray Dogs: Dead Apple",2018
    Adventure,"A Wrinkle in Time",2018
    Adventure,"Alpha",2018
    Adventure,"Annihilation",2018
    Animation,"Bungo Stray Dogs: Dead Apple",2018
    Animation,"Incredibles 2",2018
    Animation,"Isle of Dogs",2018
    Children,"A Wrinkle in Time",2018
    Children,"Incredibles 2",2018
    Children,"Solo: A Star Wars Story",2018
    Comedy,"Ant-Man and the Wasp",2018
    Comedy,"BlacKkKlansman",2018
    Comedy,"Blockers",2018
    Crime,"BlacKkKlansman",2018
    Crime,"Death Wish",2018
    Crime,"Dogman",2018
    Documentary,"Spiral",2018
    Documentary,"Won't You Be My Neighbor?",2018
    Documentary,"Blue Planet II",2017

    ...

### Show films with regular expression

`-reg | -regex <regular expression>` - Regular expression for search films by name.

Example of using the command:

    ./get-movies.sh -N 3 -reg "war"

It returns:

    genre,title,year
    Action,"Why Don't You Play In Hell? (Jigoku de naze warui)",2013
    Action,"Hardware",1990
    Action,"Swarm, The",1978
    Adventure,"Homeward Bound II: Lost in San Francisco",1996
    Adventure,"Homeward Bound: The Incredible Journey",1993
    Adventure,"Howard the Duck",1986
    Animation,"Snow White and the Seven Dwarfs",1937
    Children,"Homeward Bound II: Lost in San Francisco",1996
    Children,"Homeward Bound: The Incredible Journey",1993
    Children,"Snow White and the Seven Dwarfs",1937
    Comedy,"That Awkward Moment",2014
    Comedy,"Great Buck Howard, The",2008
    Comedy,"Benchwarmers, The",2006
    Crime,"Assassination of Jesse James by the Coward Robert Ford, The",2007
    Documentary,"Jon Stewart Has Left the Building",2015
    Documentary,"Internet's Own Boy: The Story of Aaron Swartz, The",2014
    Documentary,"Zeitgeist: Moving Forward",2011
    Drama,"Why Don't You Play In Hell? (Jigoku de naze warui)",2013
    Drama,"Assassination of Jesse James by the Coward Robert Ford, The",2007
    Drama,"Black Book (Zwartboek)",2006
    Fantasy,"Edward Scissorhands",1990
    Fantasy,"Snow White and the Seven Dwarfs",1937
    Horror,"Hardware",1990

    ...

### Sorting films by ears of release

`-yf | year_from <year>` - The Oldest year release of selected films. <p>
`-yt | year_to <year>` - the Latest year release of selected films.

Example of using the command:

    ./get-movies.sh -N 10 -reg war -yf 1990 -yt 1995

It returns:

    genre,title,year
    Action,"Hardware",1990
    Adventure,"Homeward Bound: The Incredible Journey",1993
    Children,"Homeward Bound: The Incredible Journey",1993
    Drama,"Homeward Bound: The Incredible Journey",1993
    Drama,"Howards End",1992
    Drama,"Edward Scissorhands",1990
    Fantasy,"Edward Scissorhands",1990
    Horror,"Hardware",1990
    Romance,"Edward Scissorhands",1990
    Sci-Fi,"Hardware",1990

    _

### Choose genres

`-g <genre_1|genre_2|...|genre_n>` - Select films by genres.

Example of using the command:

    ./get-movies.sh -N 10 -reg war -yf 1990 -yt 1995 -g "Drama"

It returns:

    genre,title,year
    Drama,"Homeward Bound: The Incredible Journey",1993
    Drama,"Howards End",1992
    Drama,"Edward Scissorhands",1990

    _

Another example with multiple genres.

Example of using the command:

    ./get-movies.sh -N 10 -reg war -yf 1990 -g "Drama|Children"

It returns:

    genre,title,year
    Children,"Homeward Bound II: Lost in San Francisco",1996
    Children,"Homeward Bound: The Incredible Journey",1993
    Drama,"Why Don't You Play In Hell? (Jigoku de naze warui)",2013
    Drama,"Assassination of Jesse James by the Coward Robert Ford, The",2007
    Drama,"Black Book (Zwartboek)",2006
    Drama,"Pay It Forward",2000
    Drama,"Spring Forward",1999
    Drama,"Homeward Bound: The Incredible Journey",1993
    Drama,"Howards End",1992
    Drama,"Edward Scissorhands",1990

    _

This command returns all films that have any of chosen genres begin from all drama films and ends on films for childrens.

### Additional commands

### Log errors

`-l` - command to log errors.

Example of using the command:

    ./get-movies.sh -l

If an error occurs, a `logs.log` file will be created, in which the error will be recorded.