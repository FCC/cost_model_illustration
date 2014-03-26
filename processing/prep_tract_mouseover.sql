--
-- Prepare the Mouseover used for the TileMill project
-- Assumes the tract layer is already loaded from prep_tract.py script
-- E.Spry 3/27/2014
-- 

DROP TABLE if exists analysis2014.cam_tract;

CREATE TABLE analysis2014.cam_tract
(
  state character varying(2),
  county_name character varying(50),
  tract character varying(11),
  total_locations integer,
  total_annual_support numeric,
  pc_total_locations integer,
  pc_locations_below integer,
  pc_locations_between integer,
  pc_telco_served_locations_between integer,
  pc_telco_unserved_locations_between integer,
  pc_locations_above_ttc integer,
  pc_telco_servedLocations_above_ttc integer,
  pc_telco_unserved_locations_above_ttc integer,
  pc_annual_support numeric,
  ror_total_locations integer,
  ror_locations_below integer,
  ror_locations_between integer,
  ror_telco_served_locations_between integer,
  ror_telco_unserved_locations_etween integer,
  ror_locations_above_ttc integer,
  ror_telco_served_locations_above_ttc integer,
  ror_telcoUnserved_locations_above_ttc integer,
  ror_annual_support numeric
)
WITH (
  OIDS=FALSE
);
ALTER TABLE analysis2014.cam_tract
  OWNER TO postgres;

CREATE INDEX analysis_cam_tract_tract_btree
  ON analysis2014.cam_tract
  USING btree
  (tract);

--ExperimentalTractLevelSupportBits_ParamsV3_02202014_0745AM_SR

copy analysis2014.cam_tract from 
	'/Users/ericspry/Documents/Analysis/2014/cost_model_illustration/4.1 CAM Data/ExperimentalTractLevelSupportBits.csv'
	delimiter ',' csv quote '"' header;

VACUUM ANALYZE analysis2014.cam_tract;



DROP TABLE if exists analysis2014.cam_tract_ply;

CREATE TABLE analysis2014.cam_tract_ply AS
	SELECT tract2010mb.tract, geom, gid, state, county_name, total_locations, total_annual_support,
	pc_total_locations, pc_locations_below, pc_locations_between, pc_telco_served_locations_between,
	pc_telco_unserved_locations_between, pc_locations_above_ttc, pc_telco_servedLocations_above_ttc,
	pc_telco_unserved_locations_above_ttc, pc_annual_support, ror_total_locations, ror_locations_below,
	ror_locations_between, ror_telco_served_locations_between, ror_telco_unserved_locations_etween,
	ror_locations_above_ttc, ror_telco_served_locations_above_ttc, 
	ror_telcoUnserved_locations_above_ttc, ror_annual_support
	FROM census.tract2010mb, analysis2014.cam_tract
	WHERE tract2010mb.tract=cam_tract.tract; 

CREATE INDEX cam_tract_ply_geom_gist
  ON analysis2014.cam_tract_ply
  USING gist
  (geom);
  
VACUUM ANALYZE analysis2014.cam_tract_ply;	

--
-- The End
-- 

-- Check outputs
select count(*) from analysis2014.cam_tract_ply where st_isvalid(geom) = false; 

