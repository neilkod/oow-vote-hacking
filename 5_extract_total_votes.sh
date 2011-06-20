#!/bin/bash

cd proposals 
ls -1 | while read f
do
i=$(echo $f | cut -d"-" -f1)
v=$(egrep '(people voted for this|person voted for this)' $f | perl -n -e '/<h4.*>(.*?)<\/h4>/ && print "$1"' | cut -d " " -f1)
echo "$i|$v"
done >../data/final_vote_count.dat
