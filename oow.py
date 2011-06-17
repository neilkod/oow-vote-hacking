#!/usr/bin/python
from collections import defaultdict

	
# create gephi file
out_file = open('oow.gdf', 'w')
out_file.write('nodedef> name VARCHAR, label VARCHAR, type VARCHAR\n')
person = {}
sessions = {}
votes = defaultdict(int)


# read the voters, write to a file
f = open('data/voters.dat')
for line in f:
	voter_id,voter_name = line.strip().split('|')
	voter_name = voter_name.replace('"','')
	out = "%s,%s,voter\n" % (voter_id, voter_name)
	out_file.write(out)
	person[voter_id] = voter_name
f.close()
# now do the same for sessions.
# this will be refactored ;)

# read the sessions, write to a file
# note: we're not yet interested in the actual sessions, just 
# the relationship between the voters and the session creators
# (I think...it's still early and i'm supposed to be doing something else ;) )
f = open('data/sessions.dat')
for line in f:
	session_id,session_name, session_created_by = line.strip().split('|')
	session_id = session_id * 2
	session_name = session_name.replace('"','')
	out = "%s,%s,session,%s\n" % (session_id, session_name, session_created_by)
#	out_file.write(out) 
	sessions[session_id] = {'name': session_name, 'created_by': session_created_by}
	# if the creator isn't also a voter
	# create a node for them anyway
	if session_created_by not in person.keys():
		# add the session creator to persons and the gdf file
		# note, i should made this pass first, then go through the voters
		# because not every session creator is a voter.
		person[session_created_by] = "session_creator-%s" % session_id
		out = "%s,session_creator-%s,session creator\n" % (session_created_by, session_id)
		out_file.write(out)

f.close()

# read the votes
f = open('data/votes.dat')
for line in f:
	session_id, voter_id = line.strip().split('|')
	votes[(voter_id, sessions[session_id * 2]['created_by'])] += 1
f.close()

# add nodes for people who have created a session but have not voted


out_file.write('edgedef> source VARCHAR, target VARCHAR, vote_cnt INT\n')
for (v1,v2),vote_cnt in votes.iteritems():
	out = "%s,%s,%s\n" %  (v1,v2,vote_cnt)
	out_file.write(out)


# 
# for (p1,p2),hit_count in hits.iteritems():
# 
# 	f.write('%d,%d,%d\n' % (p1,p2, hit_count ))
# f.close()


out_file.close()
