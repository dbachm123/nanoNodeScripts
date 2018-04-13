#!/bin/bash

/home/rai/stopRaiNode.sh
sleep 5s
echo "Starting node"
nohup /usr/local/bin/rai_node --daemon &
