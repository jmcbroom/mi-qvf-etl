import pandas as pd

# voters (entire_state_v.lst)
voter_schema = [
                #(column_name, start position, field length)
                ('last_name',1,35),
                ('first_name',36,20),
                ('middle_name',56,20),
                ('name_suffix',76,3),
                ('birth_year',79,4),
                ('gender',83,1),
                ('date_of_registration',84,8),
                ('house_number_character',92,1),
                ('residence_street_number',93,7),
                ('house_suffix',100,4),
                ('pre_direction',104,2),
                ('street_name',106,30),
                ('street_type',136,6),
                ('suffix_direction',142,2),
                ('residence_extension',144,13),
                ('city',157,35),
                ('state',192,2),
                ('zip',194,5),
                ('mail_address_1',199,50),
                ('mail_address_2',249,50),
                ('mail_address_3',299,50),
                ('mail_address_4',349,50),
                ('mail_address_5',399,50),
                ('voter_id',449,13),
                ('county_code',462,2),
                ('jurisdiction',464,5),
                ('ward_precinct',469,6),
                ('school_code',475,5),
                ('state_house',480,5),
                ('state_senate',485,5),
                ('us_congress',490,5),
                ('county_commissioner',495,5),
                ('village_code',500,5),
                ('village_precinct',505,6),
                ('school_precinct',511,6),
                ('permanent_absentee_ind',517,1),
                ('status_type',518,2),
                ('uocava_status',520,1)
]
voter_df = pd.read_fwf('./detroit_voters.txt',
                        colspecs=[ (r[1]-1, r[1]+r[2]-1) for r in voter_schema ],
                        names=[ r[0] for r in voter_schema ]
                      )
voter_df.to_csv('detroit_voters.csv', index=False)

# history (entire_state_h.lst)
history_schema = [
                    ('voter_id',1,13),
                    ('county_code',14,2),
                    ('jurisdiction',16,5),
                    ('school_code',21,5),
                    ('election_code',26,13),
                    ('absentee_voter_indicator',39,1),
]
history_df = pd.read_fwf('./detroit_history.txt',
                        colspecs=[ (r[1]-1, r[1]+r[2]-1) for r in history_schema ],
                        names=[ r[0] for r in history_schema ]
                      )
history_df.to_csv('detroit_history.csv', index=False)

# County codes (countycd.lst)
county_schema = [
                    ('county_code',1,2),
                    ('county_name',3,25)
]
county_df = pd.read_fwf('./FOIA_2132017/Documents/countycd.lst',
                        colspecs=[ (r[1]-1, r[1]+r[2]-1) for r in county_schema ],
                        names=[ r[0] for r in county_schema ]
                      )
county_df.to_csv('countycd.csv', index=False)


# Election Codes (electionscd.lst)
elections_schema = [
                    ('election_date_id',1,13),
                    ('election_date',14,8),
                    ('election_description',22,50)
]
elections_df = pd.read_fwf('./FOIA_2132017/Documents/electionscd.lst',
                        colspecs=[ (r[1]-1, r[1]+r[2]-1) for r in elections_schema ],
                        names=[ r[0] for r in elections_schema ]
                      )
elections_df.to_csv('electionscd.csv', index=False)


# Jurisdiction Codes (juriscd.lst)
juris_schema = [
                    ('county_code',1,2),
                    ('jurisdiction_code',3,5),
                    ('jurisdiction_name',8,35)
]
juris_df = pd.read_fwf('./FOIA_2132017/Documents/jurisdcd.lst',
                        colspecs=[ (r[1]-1, r[1]+r[2]-1) for r in juris_schema ],
                        names=[ r[0] for r in juris_schema ]
                      )
juris_df.to_csv('juriscd.csv', index=False)


# School Codes (schoolcd.lst)
school_schema = [
                    ('county_code',1,2),
                    ('jurisdiction_code',3,5),
                    ('schooldist_code',8,5),
                    ('schooldist_name',13,50)
]
school_df = pd.read_fwf('./FOIA_2132017/Documents/schoolcd.lst',
                        colspecs=[ (r[1]-1, r[1]+r[2]-1) for r in school_schema ],
                        names=[ r[0] for r in school_schema ]
                      )
school_df.to_csv('schoolcd.csv', index=False)

# Village Codes (villagecd.lst)
village_schema = [
                    ('village_id',1,13),
                    ('county_code',14,2),
                    ('jurisdiction_code',16,5),
                    ('village_dist_code',21,5),
                    ('village_name',26,50)

]
village_df = pd.read_fwf('./FOIA_2132017/Documents/villagecd.lst',
                        colspecs=[ (r[1]-1, r[1]+r[2]-1) for r in village_schema ],
                        names=[ r[0] for r in village_schema ]
                      )
village_df.to_csv('villagecd.csv', index=False)


# csv => postgresql
import odo
import sqlalchemy
engine = sqlalchemy.create_engine('postgresql://jimmy@localhost:5432/jimmy')
conn = engine.connect()

history_cols = [ "{} character varying({})".format(r[0], r[2]) for r in history_schema ]
history_ct = "create table qvf_det_history ({})".format(", ".join(history_cols))
conn.execute(history_ct)
odo.odo('./detroit_history.csv', 'postgresql://jimmy@localhost:5432/jimmy::qvf_det_history')

voter_cols = [ "{} character varying({})".format(r[0], r[2]) for r in voter_schema ]
voter_ct = "create table qvf_det_voters ({})".format(", ".join(voter_cols))
conn.execute(voter_ct)
odo.odo('./detroit_voters.csv', "postgresql://jimmy@localhost:5432/jimmy::qvf_det_voters")

county_cols = [ "{} character varying({})".format(r[0], r[2]) for r in county_schema ]
county_ct = "create table qvf_county ({})".format(", ".join(county_cols))
conn.execute(county_ct)
odo.odo('./countycd.csv', 'postgresql://jimmy@localhost:5432/jimmy::qvf_county')

elections_cols = [ "{} character varying({})".format(r[0], r[2]) for r in elections_schema ]
elections_ct = "create table qvf_elections ({})".format(", ".join(elections_cols))
conn.execute(elections_ct)
odo.odo('./electionscd.csv', 'postgresql://jimmy@localhost:5432/jimmy::qvf_elections')

juris_cols = [ "{} character varying({})".format(r[0], r[2]) for r in juris_schema ]
juris_ct = "create table qvf_juris ({})".format(", ".join(juris_cols))
conn.execute(juris_ct)
odo.odo('./juriscd.csv', 'postgresql://jimmy@localhost:5432/jimmy::qvf_juris')

school_cols = [ "{} character varying({})".format(r[0], r[2]) for r in school_schema ]
school_ct = "create table qvf_school ({})".format(", ".join(school_cols))
conn.execute(school_ct)
odo.odo('./schoolcd.csv', 'postgresql://jimmy@localhost:5432/jimmy::qvf_school')

village_cols = [ "{} character varying({})".format(r[0], r[2]) for r in village_schema ]
village_ct = "create table qvf_village ({})".format(", ".join(village_cols))
conn.execute(village_ct)
odo.odo('./villagecd.csv', 'postgresql://jimmy@localhost:5432/jimmy::qvf_village')
