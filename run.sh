#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run me as root"
  exit
fi


CURR_DIR=`pwd`
TEST_DIR=/test
BIN_DIR=/bin


echo Building container...
sudo docker build . -t expense_filer


echo Running container...
docker run \
		-v $CURR_DIR$TEST_DIR:/tmp \
		-v $CURR_DIR$BIN_DIR:/opt \
		-d -t --name expense_filer \
		expense_filer 


sudo docker exec -i -t  expense_filer /bin/sh /opt/run.sh


# echo Killing and removing container...
# sudo docker kill expense_filer
# sudo docker rm expense_filer

echo Ciao ciao!!!