# qvf

Messing around with the Michigan Qualified Voter File.

I'm working off of the `FOIA_2132017.zip` file.

My MacBook couldn't handle loading the `entire_state_v.lst` into pandas,

so this is what I did to get a subset of Detroit voters:

```
# get all detroit voters
awk '/DETROIT/' FOIA_2132017/entire_state_v.lst > ./detroit.txt
```

This also gets people that live on a `DETROIT ST` (or have `DETROIT` in their name, etc) so would want to go back through and

`delete from voters where jurisdiction not in ('22000');`

once it's in Postgres.

### 01_extract.py

Creates a `.csv` for each `.lst` file via loading into `pandas` using `read_fwf` (fixed width format.)

Additionally, can insert those .csv into Postgres using `odo`.


### a better way to convert to csv

Use `gawk` (gnu awk) to do this line by line...

```
gawk '$1=$1' FIELDWIDTHS='35 20 20 3 4 1 8 1 7 4 2 30 6 2 13 35 2 5 50 50 50 50 50 13 2 5 6 5 5 5 5 5 5 6 6 1 2 1' OFS=, entire_state_v.lst > entire_state_v.csv
```

Remove whitespace from .csv...

```
sed -e 's/  \+//g' entire_state_h.csv | sed -e 's/ \+,/,/g' > entire_state_h_trimmed.csv
```
