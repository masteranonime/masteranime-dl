#!/bin/bash

# just enough zeroes so we won't run out
ZEROES="0000000000000"
cd output || exit 1
for show in *
do
	cd "$show"
	MAX_LENGTH=0
	for episode in *
	do
		LENGTH=${#episode}
		if [ $LENGTH -gt $MAX_LENGTH ]
		then
			MAX_LENGTH=$LENGTH
		fi
	done
	for episode in *
	do
		NUM_ZEROES=`bc <<< "$MAX_LENGTH-${#episode}"`
		if [ $NUM_ZEROES -gt 0 ]
		then
			mv "$episode" "${ZEROES:0:$NUM_ZEROES}$episode"
		fi
	done
	cd ..
done
cd ..


