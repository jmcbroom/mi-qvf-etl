# qvf

Messing around with the Michigan Qualified Voter File.

My MacBook couldn't handle loading the `entire_state_v.lst` into pandas,

so this is what I did to get a subset of Detroit voters

```
# get all detroit voters
awk '/DETROIT/' FOIA_2132017/entire_state_v.lst > ./detroit.txt
```

This also gets people that live on a `DETROIT ST`, so would want to go back through and

`delete from voters where jurisdiction not in ('22000');`

once it's in Postgres.
