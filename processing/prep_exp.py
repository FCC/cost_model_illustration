## ---------------------------------------------------------------------------
###   VERSION 0.1 (for postgis)
### prep_exp.py
### Created on: Feb 19, 2014
### Created by: Michael Byrne
### Federal Communications Commission 
##
## ---------------------------------------------------------------------------


##dependencies
##software
##runs in python
##postgres/gis (open geo suite)
##the psycopg library

# Import system modules
import sys, string, os
import psycopg2
import time
now = time.localtime(time.time())
print "local time:", time.asctime(now)

#variables
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "analysis"
inTBL = "experiment"
outTBL = "exp_ply"
census = "census2010"
#http://spatialreference.org/ref/epsg/3786/
eq_prj = "3786"

#mkOutTbl - makes the output table
def mkOutTbl():
	mySQL = "DROP TABLE IF EXISTS " + schema + "." + outTBL + "; "
	mySQL = mySQL + "CREATE TABLE " + schema + "." + outTBL + " ( "
	mySQL = mySQL + "geom geometry, statefp10 character varying(2), "
	mySQL = mySQL + "myvalue integer, gid serial not null ) "
	mySQL = mySQL + " WITH ( OIDS=TRUE ); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + outTBL + " " 
	mySQL = mySQL + "OWNER TO postgres; "
	mySQL = mySQL + "CREATE INDEX " + schema + "_" + outTBL + "_geom_gist ON "
	mySQL = mySQL + schema + "." + outTBL + " USING gist (geom); COMMIT; "
	myCur = conn.cursor()	
	myCur.execute(mySQL)
	myCur.close()
	del myCur
	return

#createWorking() - makes the working table
def createWorking(myST):
	mySQL = "DROP TABLE IF EXISTS " + schema + ".working; "
	mySQL = mySQL + "CREATE TABLE " + schema + ".working as select * from "  
	mySQL = mySQL + census + ".block_" + myST + "; "
	mySQL = mySQL + "CREATE INDEX " + schema + "_working_geom_gist ON "
	mySQL = mySQL + schema + ".working USING gist (geom); "	
	mySQL = mySQL + "CREATE INDEX " + schema + "_working_geoid10_btree ON "
	mySQL = mySQL + schema + ".working USING btree (geoid10); "	
	mySQL = mySQL + "ALTER TABLE " + schema + ".working add column myvalue integer; "
	mySQL = mySQL + "COMMIT; "
	myCur = conn.cursor()	
	myCur.execute(mySQL)
	myCur.close()
	del myCur		
	return

#updateWorking() - populates the myvalue field
def updateWorking(myST):
	myCur = conn.cursor()	
	#myvalue of 1 is Served / Above 
	mySQL = "UPDATE " + schema + ".working set myvalue = 1 from "
	mySQL = mySQL + schema + "." + inTBL + " WHERE working.geoid10=" + inTBL
	mySQL = mySQL + ".geoid10 and " + inTBL + ".geoid10 like '" + myST + "%' and "
	mySQL = mySQL + "bb_served = 'S' and "
	Qrys = ["pc_rollup = 'Above';", "ror_rollup = 'Above';"]
	for myQry in Qrys:
		fullSQL = mySQL + myQry + " COMMIT; "
#		print fullSQL
		myCur.execute(fullSQL)
	#myvalue of 2 is Served / Between 
	mySQL = "UPDATE " + schema + ".working set myvalue = 2 from "
	mySQL = mySQL + schema + "." + inTBL + " WHERE working.geoid10=" + inTBL
	mySQL = mySQL + ".geoid10 and " + inTBL + ".geoid10 like '" + myST + "%' and "
	mySQL = mySQL + "bb_served = 'S' and "
	Qrys = ["pc_rollup = 'Between';", "ror_rollup = 'Between';"]
	for myQry in Qrys:
		fullSQL = mySQL + myQry + " COMMIT; "
#		print fullSQL
		myCur.execute(fullSQL)
	#myvalue of 3 is Served / Below 
	mySQL = "UPDATE " + schema + ".working set myvalue = 3 from "
	mySQL = mySQL + schema + "." + inTBL + " WHERE working.geoid10=" + inTBL
	mySQL = mySQL + ".geoid10 and " + inTBL + ".geoid10 like '" + myST + "%' and "
	mySQL = mySQL + "bb_served = 'S' and "
	Qrys = ["pc_rollup = 'Below' and ror_rollup = 'Below';", 
		"pc_rollup = 'Below' and ror_rollup = 'NA';", 
		"pc_rollup = 'NA' and ror_rollup = 'Below';"]
	for myQry in Qrys:
		fullSQL = mySQL + myQry + " COMMIT; "
#		print fullSQL
		myCur.execute(fullSQL)
	#myvalue of 4 is UNServed / Above 
	mySQL = "UPDATE " + schema + ".working set myvalue = 4 from "
	mySQL = mySQL + schema + "." + inTBL + " WHERE working.geoid10=" + inTBL
	mySQL = mySQL + ".geoid10 and " + inTBL + ".geoid10 like '" + myST + "%' and "
	mySQL = mySQL + "bb_served = 'U' and "
	Qrys = ["pc_rollup = 'Above';", "ror_rollup = 'Above';"]
	for myQry in Qrys:
		fullSQL = mySQL + myQry + " COMMIT; "
#		print fullSQL
		myCur.execute(fullSQL)
	#myvalue of 5 is UNServed / Between 
	mySQL = "UPDATE " + schema + ".working set myvalue = 5 from "
	mySQL = mySQL + schema + "." + inTBL + " WHERE working.geoid10=" + inTBL
	mySQL = mySQL + ".geoid10 and " + inTBL + ".geoid10 like '" + myST + "%' and "
	mySQL = mySQL + "bb_served = 'U' and "
	Qrys = ["pc_rollup = 'Between';", "ror_rollup = 'Between';"]
	for myQry in Qrys:
		fullSQL = mySQL + myQry + " COMMIT; "
#		print fullSQL
		myCur.execute(fullSQL)
	#myvalue of 6 is UNServed / Below 
	mySQL = "UPDATE " + schema + ".working set myvalue = 6 from "
	mySQL = mySQL + schema + "." + inTBL + " WHERE working.geoid10=" + inTBL
	mySQL = mySQL + ".geoid10 and " + inTBL + ".geoid10 like '" + myST + "%' and "
	mySQL = mySQL + "bb_served = 'U' and "
	Qrys = ["pc_rollup = 'Below' and ror_rollup = 'Below';", 
		"pc_rollup = 'Below' and ror_rollup = 'NA';", 
		"pc_rollup = 'NA' and ror_rollup = 'Below';"]
	for myQry in Qrys:
		fullSQL = mySQL + myQry + " COMMIT; "
#		print fullSQL
		myCur.execute(fullSQL)
	#myvalue of 7 is Water and not anything else 
	mySQL = "UPDATE " + schema + ".working set myvalue = 7 "
	mySQL = mySQL + " WHERE water = 1; COMMIT; "
	myCur.execute(mySQL)
	#myvalue of 8 is Unpopulated and nothing else
	mySQL = "UPDATE " + schema + ".working set myvalue = 8 "
	mySQL = mySQL + " WHERE myvalue is null; COMMIT; "
	myCur.execute(mySQL)
	myCur.close()
	del myCur	
	return

#appendOutput() - dissolves working and appends it to the output table
def appendOutput():
	mySQL = "INSERT INTO " + schema + "." + outTBL + " "
	mySQL = mySQL + "SELECT ST_UNION(geom) as geom, statefp10, myvalue "
	mySQL = mySQL + "FROM " + schema + ".working group by "
	mySQL = mySQL + "statefp10, myvalue ; COMMIT;"
	myCur = conn.cursor()	
	myCur.execute(mySQL)
	myCur.close()
	del myCur	
	return

try:
	#set up the connection to the database
	myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
	conn = psycopg2.connect(myConn)
	mkOutTbl()
	theStates = ["01","02","04","05","06","08","09"] #03, 07
	theStates = theStates + ["10","11","12","13","15","16","17","18","19"] #14
	theStates = theStates + ["20","21","22","23","24","25","26","27","28","29"]	
	theStates = theStates + ["30","31","32","33","34","35","36","37","38","39"]
	theStates = theStates + ["40","41","42","44","45","46","47","48","49"] #43
	theStates = theStates + ["50","51","53","54","55","56"] #"52"
	theStates = theStates + ["60","66","69","72","78","47"] #50

	for theST in theStates:
		print "    begining working on State: " + theST
		createWorking(theST)
		updateWorking(theST)
		print "    		...disolving..."
		appendOutput()
	now = time.localtime(time.time())
	print "local time:", time.asctime(now)
except:
	print "something bad happened"     
