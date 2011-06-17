#!/usr/bin/python
from collections import defaultdict
import operator


# note: the reason I'm multiplying session_id * 2 is because the source data
# has overlap between voter_id and session_id. Hopefully there is no
# overlap between voter_id and session_creator_id. I have not yet
# tested for that. Gephi will warn me, on the import, if we re-use
# an id.

person = {}
sessions = {}
votes = defaultdict(int)
votes_by_person = defaultdict(int)




VOTES_LIMIT = 5



# sessions first
# for the time being, we don't care about the session itself, just who 
# created it
f = open('data/sessions.dat')
for line in f:
	session_id,session_name, session_created_by = line.strip().split('|')
	session_id = int(session_id)
	session_created_by = int(session_created_by)
	
	# session name gets imported in double-quotes, lets get rid of the quotes
	session_name = session_name.split('"')[1]
	
	sessions[session_id] = {'name': session_name, 'created_by': session_created_by,'votes': 0}
	
	if session_created_by not in person.values():
		person[(session_created_by)] = {"name": "session_creator-%s" % session_id,
		 	"type" : "session creator"}
		
f.close()

# read the voters, write to a file
f = open('data/users.dat')
for line in f:
	voter_id,voter_name = line.strip().split('|')
	voter_id = int(voter_id)
	voter_name = voter_name.replace('"','')
	person[voter_id] = {"name": voter_name, "type": "voter"}
f.close()

# now that our nodes are complete, write them to the gdf file
# create gephi file, write the header
out_file = open('oow.gdf', 'w')
out_file.write('nodedef> name VARCHAR, label VARCHAR, type VARCHAR\n')

# write the nodes. leave the file open because we need to write edges
for id, vals in person.iteritems():
	out = '%s,%s,%s\n' % (id, vals['name'],vals['type'])
	out_file.write(out)

# read the votes, store in a dict where the key is (voter, session_created_by)
f = open('data/votes.dat')
for line in f:
	session_id, voter_id = line.strip().split('|')
	voter_id = int(voter_id)
	session_id = int(session_id)
	votes[(voter_id, sessions[session_id]['created_by'])] += 1
	sessions[session_id]['votes'] += 1
	
	# this might be interesting
	votes_by_person[voter_id] += 1
f.close()

# in this case, the source is the voter and the target is the session creator
out_file.write('edgedef> source VARCHAR, target VARCHAR, vote_cnt INT\n')
for (v1,v2),vote_cnt in votes.iteritems():
	out = "%s,%s,%s\n" %  (v1,v2,vote_cnt)
	out_file.write(out)

out_file.close()

# now the fun part.
# lets see who has voted for who the most times
srtd_by_votes = sorted(votes.iteritems(),key=operator.itemgetter(1))

# lets identify anyone who voted for someone else at least VOTES_LIMIT times
top_combos = [x for x in srtd_by_votes if x[1] >= VOTES_LIMIT]
print "people who have voted for someone at least %d times" % VOTES_LIMIT
for itm in top_combos:
	print "%s voted for %s %d times" % (person[itm[0][0]]['name'], person[itm[0][1]]['name'], itm[1])

# can't figure this out, don't have time
mostvotes = sorted(votes_by_person.iteritems(),key=operator.itemgetter(1))

#people who have voted the most
print ""
print "top ten voters"
print "=== === ======"
for name,votes in mostvotes[-10:]:
	print person[name]['name'], votes

print ""
# top sessions by # of votes
print "top sessions by number of votes"
print "=== ======== == ====== == ====="
xx = sorted([(v['votes'],k) for (k,v) in sessions.iteritems()])[-15:]
for v,k in xx:
	print v,sessions[k]['name'],person[sessions[k]['created_by']]['name']
