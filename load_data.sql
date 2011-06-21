-- script for MySQL

drop table sessions;
drop table votes;
drop table users;
drop table final_vote_count;

create table sessions (
session_id int primary key,
title varchar(100),
user_id int
);

create table votes (
id integer primary key auto_increment,
session_id int,
user_id int
);

create table users (
user_id int primary key,
name varchar(100)
);

create table final_vote_count (
session_id int,
total_votes int
);

LOAD DATA LOCAL INFILE 'sessions.dat' INTO TABLE sessions FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"';
LOAD DATA LOCAL INFILE 'votes.dat'    INTO TABLE votes    FIELDS TERMINATED BY '|' (session_id, user_id);
LOAD DATA LOCAL INFILE 'users.dat'    INTO TABLE users    FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"';
LOAD DATA LOCAL INFILE 'final_vote_count.dat' INTO TABLE final_vote_count FIELDS TERMINATED BY '|';
