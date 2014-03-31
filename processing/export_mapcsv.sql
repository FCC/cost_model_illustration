--
-- Create Output Table: CAM_CM_Mapping.csv
-- This script is used to dump the information used in the CAM map
-- Updated from M.Byrne on 26 March, 2014
--

ALTER TABLE analysis2014.experiment add column cost_per_loc character varying(10);

UPDATE analysis2014.experiment SET cost_per_loc = 'Above'
	WHERE pc_rollup = 'Above' OR ror_rollup = 'Above';

UPDATE analysis2014.experiment SET cost_per_loc = 'Between'
	WHERE pc_rollup = 'Between' OR ror_rollup = 'Between';


UPDATE analysis2014.experiment SET cost_per_loc = 'Below'
	WHERE (pc_rollup = 'Below' AND ror_rollup = 'Below' ) OR
		(pc_rollup = 'Below' AND ror_rollup = 'NA') OR 
		(pc_rollup = 'NA' AND ror_rollup = 'Below');

-- Final Validation check
-- should return 0 null
SELECT count(*) FROM analysis2014.experiment
	WHERE cost_per_loc is null;

-- Copy the table out to csv
--
COPY 
( SELECT state, county_name, geoid10, substr(geoid10,1,11) as tract, bb_served, 
	cost_per_loc 
	FROM analysis2014.experiment )
	TO '/Users/ericspry/Documents/Analysis/2014/cost_model_illustration/cart_data/cam_cost_map.csv'
	csv header delimiter '|';


