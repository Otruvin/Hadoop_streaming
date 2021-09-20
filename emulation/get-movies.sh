#!/bin/bash

CONFIG_FILE=.env

loadConfigFile () {
	if [ -f "$CONFIG_FILE" ];
	then 
		export $(grep -v '^#' $CONFIG_FILE | xargs)
	else
		echo "Config file doesn't exists." >&2
		exit 1
	fi
}

N=""
regexp=""
yearFrom=""
yearTo=""
genres=""
reducers=""
chunkSize=""
logs=false
help=false

#parse params from console
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -reg|--regex) 		regexp="$2"; shift ;;
		-N)					N="$2"; shift ;;
		-cz|--chunk_size)	chunkSize="$2"; shift ;;
		-r|--reducers)		reducers="$2"; shift ;;	
		-yf|--year_from)	yearFrom="$2"; shift ;;
		-yt|--year_to)		yearTo="$2"; shift ;;
		-g|--genres)		genres="$2"; shift ;;
		-l|--err_log)		logs=true ;;
		-h|--help)				help=true ;;
        *) echo "Error with parameters: $1" >&2; exit 1 ;;
    esac
    shift
done

#constract params string for get-movies.sh script
mapperArgs=""
reducerArgs=""
shaffleArgs=""
if [ "$N" != "" ]; 
then
	reducerArgs="-N $N "
fi
if [ "$regexp" != "" ]; 
then
	mapperArgs+="-reg $regexp "
fi
if [ "$yearFrom" != "" ]; 
then
	mapperArgs+="-yf $yearFrom "
fi
if [ "$yearTo" != "" ]; 
then
	mapperArgs+="-yt $yearTo "
fi
if [ "$genres" != "" ]; 
then
	mapperArgs+="-g $genres "
fi
if [ "$reducers" != "" ]; 
then
	shaffleArgs+="-r $reducers "
fi
if [ "$chunkSize" != "" ]; 
then
	mapperArgs+="-cz $chunkSize "
fi
if $logs ; 
then
	reducerArgs+="-l "
	shaffleArgs+="-l "
	mapperArgs+="-l "
fi

downloadData () {
	curl -s $URL_MOVIES -o "tmp/data.zip" > /dev/null
	pathToMovies=$(for f in tmp/data.zip; do echo "$f: "; unzip -l $f | grep "movies.csv"; done)
	pathToMovies=$(echo $pathToMovies | cut -d ' ' -f5)
	unzip -o "tmp/data.zip" $pathToMovies -d "tmp/data_temp"> /dev/null
	mv tmp/data_temp/$pathToMovies data/
	rm -rf "tmp/data_temp"
	rm "tmp/data.zip"
}

getCrcMoviesFile () {
	crcOfFindedFile=$(cksum data/movies.csv)
	crcOfFindedFile=$(echo $crcOfFindedFile | sed 's/ //g')
	echo "${crcOfFindedFile}"
}

runOrchestrationCommand () {
	cat data/movies.csv \
	| python3 mapper.py $mapperArgs \
	| sort | python3 shaffler.py $shaffleArgs \
	| python3 reducer.py $reducerArgs
}

if $help ;
then
	python3 mapper.py --help && \
	python3 shaffler.py --help && \
	python3 reducer.py --help
	exit 0
fi

loadConfigFile

if [ -f "data/movies.csv" ]; then
	crcMovies=$(getCrcMoviesFile)
	if [ "$crcMovies" = "$CRC_SMALL_MOVIES" ]; then
		runOrchestrationCommand
	else
		rm data/movies.csv
		downloadData
		runOrchestrationCommand
	fi
else
	downloadData
	runOrchestrationCommand
fi

exit 0