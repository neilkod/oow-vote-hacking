#!/bin/bash

## get the relative link to each individual proposal
cd proposal_abstracts
cat *.html | grep "<p class=\"title\">" | cut -d'"' -f4 > ../proposal_urls.txt

## download each individual proposal page
cd ../proposals
rm *
wget --no-check-certificate --base=https://mix.oracle.com/events/oow11/proposals -i ../proposal_urls.txt
