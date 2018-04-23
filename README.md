# Overview
This repository containts some helper scripts to start, stop and watch a Nano node. The main script is the watchdog script `nanoNodeWatchDog.py` which will check whether the RPC interface of the underlying Nano node is available and when the last vote of the node on the Nano network has occured. The latter is done by parsing the node's log files. The watchdog script itself will create a log file if an issue with the Nano node is detected and restart the node automatically. 

# Setup

`nanoNodeWatchDog.py` is designed to be run as a [cronjob](https://help.ubuntu.com/community/CronHowto), e.g. by adding the following to your crontab (of course, you can run it manually from a terminal first, to check if it is working correctly):

``` 
# m h  dom mon dow   command
*/2 *  * * * /home/rai/cron/nanoNodeWatchDog.py
``` 

You will have to edit some variables in the `main()` function of `nanoNodeWatchDog.py` and adapt them to your local Nano node setup: 
``` 
# --------------------------------------------------
# some variables - adapt these to your local node setup
nodeIP = '[::1]' # node's local IP
nodePort = '7076' # RPC port
startScript = "/home/rai/startRaiNode.sh" # script to (re)-start Nano node
logFile = "/home/rai/nanoNode.log" # log file for this script 
nodeLogDir = "/home/rai/RaiBlocks/log" # the log directory of the Nano node
# --------------------------------------------------
```
Also, have a look at `startRaiNode.sh` and `stopRaiNode.sh` which you will have to adapt as well in terms of paths. 

# Log File
The log file of `nanoNodeWatchDog.py` will look as follows:

``` 
2018-04-18 11:09:07.806252 ::: RPC not available
2018-04-18 11:09:07.814590 ::: Restarting node
2018-04-18 11:25:03.086756 ::: Last vote was 501.716614 seconds ago
2018-04-18 11:25:03.094466 ::: Restarting node
```

# Contribute

Feel free to send an [issue](https://github.com/dbachm123/nanoNodeScripts/issues) or a pull request. 
My rep node and donations: *xrb_1f56swb9qtpy3yoxiscq9799nerek153w43yjc9atoaeg3e91cc9zfr89ehj* (http://138.197.179.164/)




