#!/bin/bash
#
set -e
if [ -a /home/pi/scripts/transfer.ok ]; then
	python /home/pi/scripts/gensqlsensordata.py /home/pi/repository/LOG.txt > /home/pi/repository/sensordata.sql 
	rm /home/pi/scripts/transfer.ok
else
	python /home/pi/scripts/gensqlsensordata.py /home/pi/repository/LOG.txt >> /home/pi/repository/sensordata.sql 
fi

scp [credentials] /home/pi/repository/sensordata.sql [login]@[server]:incoming/office126/
echo $(date) > /home/pi/scripts/transfer.ok

#rm /home/pi/repository/LOG.txt
