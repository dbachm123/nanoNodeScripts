#!/bin/bash

$HOME/stopBananoNode.sh
sleep 5s
echo "Starting node"
docker run -d --restart unless-stopped -p 7071:7071/udp -p 7071:7071 -p [::1]:7072:7072 -v ~:/root bananocoin/banano:latest
