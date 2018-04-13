#!/usr/bin/python3

import requests
from subprocess import call
import datetime
import glob
import os
import sys
import re
from datetime import datetime, timedelta




# test RPC
def testRPC(ip, port, logFile):
	# test RPC
	try:
		data = '{"action": "version"}'
		response = requests.post('http://{}:{}'.format(ip,port), data=data, timeout=5)
		return response.status_code == requests.codes.ok
	except Exception as e:
		log("RPC not available", logFile)
		return False


# check when the latest vote occured
def testVoting(ip, port, latestNodeLog, logFile):

	# maximum allowed time in seconds since last vote
	maxSecondsSinceLastVote = 5 * 60; # 5 minutes

	# check for the timestamp of the following message in the log
	msgInLog = "was confirmed to peers";

	# read file line by line; start at the back
	with open(latestNodeLog) as fp:
		cnt = 0
		for line in reversed(list(fp)):
			if msgInLog in line:
				# found a line --> extract time stamp
				# line is something like:
				# [[2018-04-13 08:37:48.001414]: Block D84B7B...  was confirmed to peers

				match = re.search(r'\[(.*?)\]', line)
				if match:
					timestamp = match.group(1)
					if timestamp:
						# convert timestamp to datetime object
						dateFormat = '%Y-%m-%d %H:%M:%S.%f'
						voteTime = datetime.strptime(timestamp, dateFormat)

						# check when the last vote was
						now = datetime.now()
						lastVoteSecondsAgo = (now - voteTime).total_seconds()
						if (lastVoteSecondsAgo > maxSecondsSinceLastVote):
							log("Last vote was {} seconds ago".format(lastVoteSecondsAgo), logFile);
							return False;
				break
	return True
	

# log
def log(message, logFile):
	now = datetime.now()
	print("{} ::: {}".format(now, "{}".format(message)), file=open(logFile, "a"))


# check whether node is alive
def nodeAlive(ip, port, latestNodeLog, logFile):
	
	# run all tests
	ret = True;
	ret = ret & testRPC(ip, port, logFile);
	ret = ret & testVoting(ip, port, latestNodeLog, logFile);
	return ret


# find latest file in directory
def findLatestFileInDir(dir):
	
	list_of_files = glob.glob(dir+'/*.log') 
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file
	

# restart node
def restartNode(startScript, logFile):

	# log and restart
	log("Restarting node", logFile)
	call(["bash", startScript])

# main
def main():

	# some variables
	nodeIP = '[::1]'
	nodePort = '7076'
	startScript = "/home/rai/startRaiNode.sh"
	logFile = "/home/rai/nanoNode.log"
	nodeLogDir = "/home/rai/RaiBlocks/log"

	# find latest log file in the node's log dir
	latestNodeLog = findLatestFileInDir(nodeLogDir)

	# check node running
	nodeRunning = nodeAlive(nodeIP, nodePort, latestNodeLog, logFile)

	if not nodeRunning:		
		restartNode(startScript, logFile)



if __name__ == "__main__":
    main()

