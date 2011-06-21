select  repeat(concat(replace(lower(a.title),'oracle',' '),' '),b.total_votes)
  from  sessions a
     ,  final_vote_count b
 where  a.session_id = b.session_id;
