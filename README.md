# nanoNodeScripts
Some helper scripts to start, stop and watch a Nano node. Run this as a [cronjob](https://help.ubuntu.com/community/CronHowto), e.g. add the following to your crontab. 

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


# Contribute

My rep node and donations: xrb_1f56swb9qtpy3yoxiscq9799nerek153w43yjc9atoaeg3e91cc9zfr89ehj (http://138.197.179.164/)




