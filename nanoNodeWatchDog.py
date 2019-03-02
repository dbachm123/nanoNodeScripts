#!/usr/bin/python3

# Run this via cron, e.g. with the following entry in crontab:
# # m h  dom mon dow   command
# */1 * * * * /etc/cron.hourly/nanoNodeWatchDog.py

import requests
from subprocess import call
import datetime
import glob
import os
import sys
import re
from datetime import datetime, timedelta
from os.path import expanduser

# test whether RPC is responsive
def testRPC(ip, port, logFile):
    # test RPC
    try:
        data = '{"action": "version"}'
        response = requests.post('http://{}:{}'.format(ip,port), data=data, timeout=5)
        return response.status_code == requests.codes.ok
    except Exception as e:
        log("RPC not available", logFile)
        return False

# test when the latest vote occured
def testVoting(ip, port, latestNodeLog, logFile):
    # maximum allowed time in seconds since last vote
    maxSecondsSinceLastVote = 5 * 60; # 5 minutes

    # check for the timestamp of the following message in the log
    msgInLog1 = "Broadcasting confirm req for";
    msgInLog2 = "was republished to peers";

    # read file line by line; start at the back
    with open(latestNodeLog) as fp:
        cnt = 0
        for line in reversed(list(fp)):
            if msgInLog1 in line or msgInLog2 in line:
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

# log a message to logFile
def log(message, logFile):
    now = datetime.now()
    print("{} ::: {}".format(now, message), file=open(logFile, "a"))

# check whether the node is alive
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

    home = expanduser("~")

    # --------------------------------------------------
    # some variables - adapt these to your local node setup
    nodeIP = '[::1]' # node's local IP
    nodePort = '7076' # RPC port
    startScript = "{}/startRaiNode.sh".format(home) # script to (re)-start Nano node
    logFile = "{}/nanoNode.log".format(home)  # log file for this script 
    nodeLogDir = "{}/Nano/log".format(home)  # the log directory of the Nano node
    # --------------------------------------------------

    # find latest log file in the node's log dir
    latestNodeLog = findLatestFileInDir(nodeLogDir)

    # check whether node is alive and restart if it is not
    if (not nodeAlive(nodeIP, nodePort, latestNodeLog, logFile)):
        restartNode(startScript, logFile)


if __name__ == "__main__":
    main()

