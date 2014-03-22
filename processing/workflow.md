## workflow.md

This describes the workflow for the steps to create the cost experiment map.  The resulting map is a 6 color map.  The legend is made by aggregating the fields bb_served (e.g. wether or not the block is currently served by broadband) and the combination of values in the pc_rollup and ror_rollup.  So you end up with something like this:
<table>
	<tr><td>Block Broadband Condition</td><td>Costs Per Location in the block</td></tr>
    <tr><td>Block is Served</td><td>Block has Price Cap and Rate of return costs ABOVE the threshhold</td></tr>
    <tr><td>Block is Served</td><td>Block has Price Cap and Rate of return costs BETWEEN the threshhold</td></tr>
    <tr><td>Block is Served</td><td>Block has Price Cap and Rate of return costs BELOW the threshhold</td></tr>
    <tr><td>Block is Not Served</td><td>Block has Price Cap and Rate of return costs ABOVE the threshhold</td></tr>
    <tr><td>Block is Not Served</td><td>Block has Price Cap and Rate of return costs BETWEEN the threshhold</td></tr>
    <tr><td>Block is Not Served</td><td>Block has Price Cap and Rate of return costs BELOW the threshhold</td></tr>
</table>

Step 1 - Input Source Data
--------------------------
Import the source block cost data from Cost Quest into a postgres table.  This data comes as a csv of blocks.  The (SQL script)[https://github.com/fccdata/cost_model_illustration/blob/master/processing/import_experiment.sql] loads the data into postgres.  The last command in this scriot demonstrates the variation of the fields 'Served' and 'Rollup' used to make the legend so one can understand the number of records for these selections.  Typically CQ delivers only blocks w/ population so it is far lower than the 11 million row count of all blocks.

Step 2 - Make geospatial table from Source Data
-----------------------------------------------
Run the (python script)[https://github.com/fccdata/cost_model_illustration/blob/master/processing/prep_exp.py].  This script works on the premise that (a) one has a library of blocks as individual state block tables and (b) there is a set of water and coastline attributes on the block.  The script has 4 basic parts.
- Part 1 - mkOutTbl() - This part creates an output table which will contain the fields, gid, state_fips, myvalue and geom.  myvalue will be 1 through 6 (e.g. the legend above).  state_fips will be the two digit state fips code. All resulting data is poured into this output table for display in the final product.
- Part 2 - createWorking(theST) - This part creates a working dataset of the current loop of a state block table.  It then adds a field called myvalue which ends up becoming the legend.
- Part 3 - updateWorking(theST) - This part is the real driver.  It updates the myvalue based on the 6 relative categories required to make the legend.  These 6 categories are displayed in the table above.  Served is very easy, but pc_rollup and ror_rollup, end up being quite complicated.  This complication is the result of some locations w/i an individual block can be either PC or ROR locations.  This part of the script has a sub loop which selects a hierarchy of these locations as part of the myvalue field setting.  Generally speaking Above and Between values are easy, but below threshholds are complicated.  In this step all water polygons end up w/ their own value (eg myvalue = 7).
- Part 4 - appendOutput() - This part dissolves (eg st_union) the working table updated in Part 3, on the myvalue and state_fips field AND inserts the results into the output table created in Part 1.

Notes
-----
- When running this, it is worth it to make sure the sub-loops described in Part 3 of Step 2 contain all of the possible variation that was the result of the last command in Step 1 (the group by query at the end of the load scrip).  If the subloops do not describe all the variation, just add one to lines that begin w/ 'Qrys'.
- I have tended to run Step 2 first with a test state like DE or RI (a small state). When it completes it is helpful to open this in say QGis/TileMill to see what the result looks like, and is right (e.g. test some blocks w/ the categories to make sure it worked).  This is advantageous, b/c the script takes a long time to run and you want to be right the first time.
- If you have stopped the script for a certain number of states and want to rerun it later w/ other states, be sure to comment out the line 'mkOutTbl()' becuase this will erase all previous work.

Colors and Legend
-----------------
Here are the resulting colors and field values for the legend.
<table>
	<tr>
    	<td>Block Broadband Condition</td><td>Costs Per Location in the block</td><td>myvalue</td><td>hex color</td>
        <td>Block is Served</td><td>Block has Price Cap and Rate of return costs ABOVE the threshhold</td><td>1</td><td>#FFACA1</td>
        <td>Block is Served</td><td>Block has Price Cap and Rate of return costs BETWEEN the threshhold</td><td>2</td><td>#C4F489</td>
        <td>Block is Served</td><td>Block has Price Cap and Rate of return costs BELOW the threshhold</td><td>3</td><td>#FBDA62</td>
        <td>Block is Not Served</td><td>Block has Price Cap and Rate of return costs ABOVE the threshhold</td><td>4</td><td>#DC4E3D</td>
        <td>Block is Not Served</td><td>Block has Price Cap and Rate of return costs BETWEEN the threshhold</td><td>5</td><td>#28925B</td>
        <td>Block is Not Served</td><td>Block has Price Cap and Rate of return costs BELOW the threshhold</td><td>6</td><td>#D99442</td>
        <td>N/A</td><td>Water</td><td>7</td><td>#DEEDEF</td>
    </tr>
</table>



 
