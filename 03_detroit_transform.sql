create index qvf_det_voters_id_idx on qvf_det_voters using btree(voter_id);
create index qvf_det_history_id_idx on qvf_det_history using btree(voter_id);

alter table qvf_det_voters
  alter date_of_registration
  type timestamp
  using(to_date(lpad(date_of_registration, 8, '0'), 'MMDDYYYY'));

alter table qvf_det_voters 
  add column num_votes integer;
update qvf_det_voters
  set num_votes = (select count(*)
                    from qvf_det_history
                    where qvf_det_history.voter_id = qvf_det_voters.voter_id);
