import sys


if len(sys.argv) < 2:
    sys.exit('Usage: %s logfile' % sys.argv[0])

#sensor id settings in sensors.setup
fpar = open("sensors.setup", "r")
params = [[]]
labels = fpar.readline()
params[0] = labels.rstrip().split(":")
ntypes = len(params[0])

#gateway:board:sensorid:TE:HU:CO2:LT:PT
##office 126 - gateway 1
#1:1:2:2:3::4
#1:2:3:5:6:7:
#1:3:4:8:9::

h = 0
for lines in fpar:
	if lines.find("#",0) == -1:
		params.append(lines.rstrip().split(":")) 
		h = h + 1

nboards = h

#print params
#print "sensor types: " + str(ntypes-1)
#print "number of sensor boards collected from this rpi " + str(nboards)

##2015-05-02 18:00:50.526487    GT:1#ID:8#BT:55#PT:24.87
##2015-05-02 18:01:15.750777    GT:3#ID:4#BT:16#TE:20.64#HU:45.99#CO2:1.47
##2015-05-02 18:01:54.674796    GT:3#ID:1#BT:48#TE:23.22#HU:39.75#LT:2.40


flog = open(sys.argv[1], "r")

nreadings = 0
for lines in flog:
	lines = lines.replace("  ", " ")
	lines = lines.replace("  ", " ")
	chunks = lines.split(" ")
	if len(chunks) == 1:
		break
	date = chunks[0]
	timefull = chunks[1].split(".")
	time = timefull[0]
	time = time[:5]

	info = chunks[2].split("#")
	#print info  
	#all chunks
	gateway = info[0].split(":")
	gid = gateway[1]

	board = info[1].split(":")
	bid = board[1]

	battery = info[2].split(":")
	batterylevel = battery[1]

	n = len(info)
	i = 3	#the first real sensed data in a reading
	while i < n:
		measure = info[i].split(":")
		mid = measure[0]
		#find the order of the physical value in the sequence
		col = -1
		for j in range(ntypes):
			if params[0][j] == measure[0]:
				col = j
				break
		#find the ID of the specific value reading in sensors.setup
		row = -1
		for j in range(nboards+1):
			if params[j][0] == gid and params[j][1] == bid:
				row = j
				break
		if col > -1 and row > -1:
			mval = measure[1]
			mval = mval.rstrip()
			variableid = params[row][col]
			sensorid = params[row][2]
			sqlstr = "INSERT INTO measurement(date,time,value,fkvariable) VALUES ('%s', '%s:00', %s, %s);" % (date, time, mval, variableid)
			print sqlstr
			i = i + 1
		else:
			print "Impossible to find match for meaasure % for sensor %" % (measure[0], bid)

	#update also battery level
	sqlstr = "UPDATE sensor SET batterylevel=" + batterylevel + " WHERE sensorid=" + sensorid + ";"
	print sqlstr
	nreadings = nreadings + 1

#print "Readings: " + str(nreadings)