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
output=""
logs=false
help=false

#parse params from console
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --output)			output="$2"; shift ;;
        -reg|--regex) 		regexp="$2"; shift ;;
		-N)					N="$2"; shift ;;
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
if $logs ; 
then
	reducerArgs+="-l "
	mapperArgs+="-l "
fi

putDataToHDFS () {
	hdfs dfs -put $1 /tmp/data_movies.csv > /dev/null
}

catMoviesData () {
	hdfs dfs -cat /tmp/output_movies/*
}

deleteTempData () {
	hdfs dfs -rm -r /tmp/output_movies > /dev/null
}

checkIfMoviesFileExists () {
	hdfs dfs -test -e /tmp/data_movies.csv && echo $?
}

getCrcMoviesData () {
	hdfs dfs -checksum /tmp/data_movies.csv | tr -d '[:space:]'
}

removeMoviesDataFromHDFS () {
	hdfs dfs -rm /tmp/data_movies.csv > /dev/null
}

runHadoopProcess () {
	yarn jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
	-input /tmp/data_movies.csv \
	-output /tmp/output_movies \
	-file mapper.py \
	-file reducer.py \
	-mapper "python mapper.py ${mapperArgs}" \
	-reducer "python reducer.py ${reducerArgs}" &>/dev/null
}

downloadData () {
	curl -s $URL_MOVIES -o "tmp/data.zip" > /dev/null
	pathToMovies=$(for f in tmp/data.zip; do echo "$f: "; unzip -l $f | grep "movies.csv"; done)
	pathToMovies=$(echo $pathToMovies | cut -d ' ' -f5)
	unzip -o "tmp/data.zip" $pathToMovies -d "tmp/data_temp"> /dev/null
	putDataToHDFS tmp/data_temp/$pathToMovies
	rm -rf "tmp/data_temp"
	rm "tmp/data.zip"
}

if $help ;
then
	python3 mapper.py --help && \
	python3 reducer.py --help
	exit 0
fi

loadConfigFile

if [ "$(checkIfMoviesFileExists)" = "0" ]; then
	if [ "$(getCrcMoviesData)" = "$CRC_SMALL_MOVIES" ]; then
		runHadoopProcess
		catMoviesData
		deleteTempData
	else
		removeMoviesDataFromHDFS
		downloadData
		runHadoopProcess
		catMoviesData
		deleteTempData
	fi
else
	downloadData
	runHadoopProcess
	catMoviesData
	deleteTempData
fi

exit 0
