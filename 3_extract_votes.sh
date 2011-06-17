#!/bin/bash

## clean up old vote extract
cd votes
rm *
cd ..

## extract the voters from each proposal and put them in a file 1 per proposal
cd proposals

ls -1 | while read f
do
grep voting $f | grep 0px  | cut -d'"' -f2 | cut -d "/" -f6 > ../votes/$f.txt
done