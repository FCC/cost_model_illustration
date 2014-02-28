## ---------------------------------------------------------------------------
###   VERSION 0.1 (for postgis)
### prep_tract.py
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
schema = "carto"
inTBL = "experiment"
outTBL = "tract"
census = "census2010"
#http://spatialreference.org/ref/epsg/3786/
eq_prj = "3786"

#mkOutTbl - makes the output table
def mkOutTbl():
	mySQL = "DROP TABLE IF EXISTS " + schema + "." + outTBL + "; "
	mySQL = mySQL + "CREATE TABLE " + schema + "." + outTBL + " ( "
	mySQL = mySQL + "geom geometry, statefp10 character varying(2), "
	mySQL = mySQL + "tract character varying(11), "
	mySQL = mySQL + "myvalue integer, gid serial not null ) "
	mySQL = mySQL + " WITH ( OIDS=TRUE ); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + outTBL + " " 
	mySQL = mySQL + "OWNER TO postgres; "
	mySQL = mySQL + "CREATE INDEX " + schema + "_" + outTBL + "_geom_gist ON "
	mySQL = mySQL + schema + "." + outTBL + " USING gist (geom); COMMIT; "
	myCur.execute(mySQL)
	return

#appendOutput() - dissolves working and appends it to the output table
def appendOutput(myST):
	mySQL = "INSERT INTO " + schema + "." + outTBL + " "
	mySQL = mySQL + "SELECT ST_UNION(geom) as geom, statefp10, "
	mySQL = mySQL + " substr(geoid10, 1, 11) as tract "
	mySQL = mySQL + "FROM " + census + ".block_" + myST 
	mySQL = mySQL + " WHERE nearshore = 0"
	mySQL = mySQL + " group by "
	mySQL = mySQL + "statefp10, tract ; COMMIT;"
	print mySQL	
	myCur.execute(mySQL)	
	return

try:
	#set up the connection to the database
	theConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
	conn = psycopg2.connect(theConn)
	myCur = conn.cursor()	
	mkOutTbl() #, 04, "22",
	theStates = ["01","02","04","05","06","08","09"] #03, 07
	theStates = theStates + ["10","11","12","13","15","16","17","18","19"] #14
	theStates = theStates + ["20","21","22","23","24","25","26","27","28","29"]	
	theStates = theStates + ["30","31","32","33","34","35","36","37","38","39"]
	theStates = theStates + ["40","41","42","44","45","46","47","48","49"] #43
	theStates = theStates + ["50","51","53","54","55","56"] #"52"
	theStates = theStates + ["60","66","69","72","78"] #50
	for theST in theStates:
		print "    begining working on State: " + theST
		appendOutput(theST)
	del myCur
	now = time.localtime(time.time())
	print "local time:", time.asctime(now)
except:
	print "something bad happened"     
