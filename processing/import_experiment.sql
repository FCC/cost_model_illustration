drop table if exists analysis.experiment;

CREATE TABLE analysis.experiment
(
	state character varying(2),
	county_name character varying(30),
	geoid10 character varying(15),
	total_locations integer,
	bb_served character varying(1),
	pc_total_locations integer,
	pc_locations_below integer,
	pc_telco_served_locations_below integer,
	pc_telco_unserved_locations_below integer,
	pc_locations_between integer,
	pc_telco_served_locations_between integer,
	pc_telco_unserved_locations_between integer,
	pc_locations_above_ttc integer,
	pc_telco_served_locations_above_ttc integer,
	pc_telco_unserved_location_above_ttc integer,
	pc_rollup character varying(7),
	ror_total_locations integer,
	ror_locations_below integer,
	ror_telco_served_locations_below integer,
	ror_telco_unserved_locations_below integer,
	ror_locations_between integer,
	ror_telco_served_locations_between integer,
	ror_telco_unserved_locations_between integer,
	ror_locations_above_ttc integer,
	ror_telco_served_locations_above_ttc integer,
	ror_telco_UnservedLocations_above_ttc integer,
	ror_rollup character varying(7)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE analysis.experiment
  OWNER TO postgres;

copy analysis.experiment
	from '/Users/feomike/documents/analysis/2014/experiment/ExperimentalCBMappingSupportBits_ParamsV3_02192014_0330PM_US/ExperimentalCBMappingSupportBits_ParamsV3_02192014_0330PM_US.csv'
	csv header delimiter ',' quote '"';

create index analysis_experiment_geoid10_btree
	on analysis.experiment
	using btree (geoid10);
	
select bb_served, pc_rollup, ror_rollup, count(*) 
	from analysis.experiment 
	group by bb_served, pc_rollup, ror_rollup
