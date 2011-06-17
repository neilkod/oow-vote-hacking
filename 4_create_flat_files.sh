#!/bin/bash

## flat file for sessions
## format session_id|"title"|user_id

cd proposals
ls -1 | while read f
do
sid=$(echo $f | cut -d"-" -f1)
t=$(grep h2 $f | perl -n -e '/<h2>(.*?)<\/h2>/ && print "$1\n"')
aid=$(grep presenter-type $f | cut -d'"' -f2| cut -d"/" -f6)
echo "${sid}|\"${t}\"|${aid}"
done > ../data/sessions.dat
cd ..

## flat file for users (assumed to be a unique list of all voters)
## format user_id|"name"

cd votes
cat * | sort -n -u | while read f
do
id=$(echo $f|cut -d"-" -f1)
n=$(echo $f|cut -d"-" -f2-|sed "s/-/ /g")
echo "$id|\"$n\""
done > ../data/users.dat
cd ..

## flat file for votes
## format session_id|user_id

cd votes
ls -1 | while read f
do
s=$(echo $f |cut -d"-" -f1)
cat $f | while read l
do
v=$(echo $l | cut -d"-" -f1)
echo "$s|$v"
done
done > ../data/votes.dat
