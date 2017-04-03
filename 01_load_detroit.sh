awk 'substr($0, 464, 5) ~ 22000' ./FOIA_2132017/entire_state_v.lst > detroit_voters.txt
awk 'substr($0, 16, 5) ~ 22000' ./FOIA_2132017/entire_state_h.lst > detroit_history.txt
