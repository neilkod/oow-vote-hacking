#!/bin/bash

## as of June 17th there are 39 pages of proposals sorted by title
## as of June 19th there are 41 pages of proposals sorted by title
## final count are 43 pages of proposals sorted by title
## see https://mix.oracle.com/events/oow11/proposals to determine this value

cd proposal_abstracts
rm *.html
for i in {1..43}
do
curl -o $i.html "https://mix.oracle.com/events/oow11/proposals?campaign_id=oow11&page=${i}&sort=title"
done
