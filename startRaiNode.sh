#!/bin/bash

$HOME/stopRaiNode.sh
sleep 5s
echo "Starting node"
nohup /usr/local/bin/nano_node --daemon &
